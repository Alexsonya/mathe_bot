# Deploying mathe_bot to a Hetzner VPS

End state: a small Linux server runs `bot.py` under `systemd` 24/7, and every push to `main` on GitHub redeploys it automatically.

Estimated cost: ~€4/month for the smallest Hetzner Cloud tier (CX22 or CAX11). Setup time: ~30 minutes.

---

## 0. Prerequisites

- A bot token from [@BotFather](https://t.me/BotFather) (already in your local `.env`).
- A [Hetzner Cloud](https://console.hetzner.cloud/) account.
- A GitHub repo you can push to (yours: `Alexsonya/mathe_bot`).
- A local Linux/macOS shell with `ssh`, `ssh-keygen`, and `git`.

---

## 1. Create your personal SSH key pair (local)

This is the key *you* use to log into the server. Skip this step if you already have an Ed25519 key at `~/.ssh/id_ed25519`.

```bash
ssh-keygen -t ed25519 -C "you@example.com" -f ~/.ssh/id_ed25519
```

- Pick a strong passphrase when prompted (or none if you'll add it to `ssh-agent`).
- This creates two files:
  - `~/.ssh/id_ed25519` — **private**, never share, never commit.
  - `~/.ssh/id_ed25519.pub` — public, safe to paste anywhere.

Show the public key so you can copy it:
```bash
cat ~/.ssh/id_ed25519.pub
```

> Ed25519 is preferred over RSA — shorter keys, faster, and considered modern-secure.

---

## 2. Provision the Hetzner VPS

1. Open <https://console.hetzner.cloud/> → **New Project** → **Add Server**.
2. **Location**: pick the one nearest you (Nuremberg, Falkenstein, or Helsinki are EU; Ashburn/Hillsboro for US).
3. **Image**: **Ubuntu 24.04**.
4. **Type**:
   - **CAX11** (ARM, 2 vCPU, 4 GB RAM) — cheapest, ~€3.79/mo. Works fine for a Telegram bot.
   - or **CX22** (Intel/AMD, 2 vCPU, 4 GB RAM) — ~€4.51/mo, use this if you ever need x86-only Python wheels.
5. **Networking**: keep **IPv4 + IPv6**. The IPv4 Primary IP costs ~€0.71/month (€0.00097/h) on top of the server. It looks tempting to go IPv6-only and save it, but **GitHub Actions runners are IPv4-only** — without a Primary IPv4 the CI/CD workflow can't SSH into the server. Home/mobile ISP v6 reachability is also unreliable, so your own SSH access benefits from v4 too.
6. **SSH keys**: **Add SSH Key** → paste the contents of `~/.ssh/id_ed25519.pub` → name it `personal-laptop`.
7. **Name**: `mathe-bot`.
8. Click **Create & Buy now**.

After ~10 seconds you get a public IPv4 like `203.0.113.42`. Note it down — referred to below as `$SERVER_IP`.

---

## 3. First login and base hardening

Log in as root (Hetzner pre-installs your public key, so no password prompt):

```bash
ssh root@$SERVER_IP
```

On first connection accept the host fingerprint (`yes`). Then on the server:

```bash
apt update && apt upgrade -y
apt install -y python3-venv git ufw fail2ban

# Firewall: SSH only, deny everything else inbound
ufw allow OpenSSH
ufw --force enable

# fail2ban watches SSH logs and bans IPs that brute-force
systemctl enable --now fail2ban
```

Disable password logins and root login over SSH:

```bash
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh
```

`PermitRootLogin prohibit-password` keeps root SSH possible *only with the key* — you'll lock down further once the deploy user exists.

---

## 4. Create the `mathebot` deploy user

Still as root on the server:

```bash
adduser --disabled-password --gecos "" mathebot

# Copy your personal SSH key over so you can log in as mathebot
mkdir -p /home/mathebot/.ssh
cp /root/.ssh/authorized_keys /home/mathebot/.ssh/authorized_keys
chown -R mathebot:mathebot /home/mathebot/.ssh
chmod 700 /home/mathebot/.ssh
chmod 600 /home/mathebot/.ssh/authorized_keys
```

Grant **only one** passwordless sudo command — restarting the service. CI/CD needs this; nothing else should be sudoable without a password.

```bash
cat >/etc/sudoers.d/mathebot <<'EOF'
mathebot ALL=(root) NOPASSWD: /usr/bin/systemctl restart mathe-bot, /usr/bin/systemctl is-active mathe-bot, /usr/bin/systemctl status mathe-bot
EOF
chmod 440 /etc/sudoers.d/mathebot
visudo -c   # validates all sudoers files; must say "parsed OK"
```

Test from a **second terminal on your laptop** (don't close the root session yet):

```bash
ssh mathebot@$SERVER_IP
```

If that works, you can later switch root SSH off entirely (`PermitRootLogin no`).

---

## 5. Clone the repo and install dependencies

As `mathebot` on the server:

```bash
cd ~
git clone https://github.com/Alexsonya/mathe_bot.git
cd mathe_bot
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

---

## 6. Set up `.env` on the server

Never commit the token. Create `.env` manually on the server:

```bash
cat >~/mathe_bot/.env <<EOF
TELEGRAM_BOT_TOKEN=123456:replace-with-your-real-token
EOF
chmod 600 ~/mathe_bot/.env
```

---

## 7. Install the systemd service

The repo ships `deploy/mathe-bot.service`. Install it as **root** (use `sudo -i` from your own user if root SSH is off):

```bash
cp /home/mathebot/mathe_bot/deploy/mathe-bot.service /etc/systemd/system/mathe-bot.service
systemctl daemon-reload
systemctl enable --now mathe-bot
systemctl status mathe-bot
```

Live logs:
```bash
journalctl -u mathe-bot -f
```

Common operations:
```bash
sudo systemctl restart mathe-bot     # apply config/code change
sudo systemctl stop mathe-bot        # take offline
journalctl -u mathe-bot --since "1 hour ago"
```

At this point the bot is live on Telegram. Message it to confirm.

---

## 8. Set up CI/CD (GitHub Actions)

The workflow at `.github/workflows/deploy.yml` does, on every push to `main`:
1. Syntax-checks the Python files.
2. SSHs into the server as `mathebot`, pulls, reinstalls deps, restarts the service.

### 8a. Create a **separate** deploy key

Don't reuse your personal key for CI. Generate a dedicated key *on your laptop*:

```bash
ssh-keygen -t ed25519 -C "github-actions-mathe-bot" -f ~/.ssh/mathe_bot_deploy -N ""
```

(`-N ""` skips the passphrase — required because GitHub Actions can't type one.)

Append the new public key to `mathebot`'s authorized keys on the server:

```bash
cat ~/.ssh/mathe_bot_deploy.pub | ssh mathebot@$SERVER_IP 'cat >> ~/.ssh/authorized_keys'
```

### 8b. Capture the server's host key

So GitHub Actions doesn't get a "host key verification" prompt:

```bash
ssh-keyscan -t ed25519 $SERVER_IP
```

Copy the single-line output.

### 8c. Add four GitHub secrets

In your repo on github.com → **Settings → Secrets and variables → Actions → New repository secret**. Add:

| Name              | Value                                                            |
|-------------------|------------------------------------------------------------------|
| `SSH_HOST`        | the server IP, e.g. `203.0.113.42`                               |
| `SSH_USER`        | `mathebot`                                                       |
| `SSH_PRIVATE_KEY` | contents of `~/.ssh/mathe_bot_deploy` (the **private** half)     |
| `SSH_KNOWN_HOSTS` | the line you got from `ssh-keyscan`                              |

> When pasting `SSH_PRIVATE_KEY`, include the `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----` lines and the trailing newline.

### 8d. Trigger the first deploy

Push any change to `main`, or run **Actions → deploy → Run workflow** manually. Watch the run; the `Pull and restart on Hetzner` step should end with `active`.

---

## 9. (Recommended) Add persistence so scores survive restarts

Right now every restart wipes `ctx.user_data` and the daily-task lockout. Three-line fix in `bot.py`:

```python
from telegram.ext import PicklePersistence

persistence = PicklePersistence(filepath="bot_data.pickle")
app = Application.builder().token(TOKEN).persistence(persistence).build()
```

Add `bot_data.pickle` to `.gitignore` — it shouldn't end up in git.

---

## 10. Day-to-day operations cheat sheet

```bash
# SSH in
ssh mathebot@$SERVER_IP

# Tail logs
journalctl -u mathe-bot -f

# Force redeploy without pushing (run on server)
cd ~/mathe_bot && git pull && .venv/bin/pip install -r requirements.txt && sudo systemctl restart mathe-bot

# Rollback to previous commit (run on server)
cd ~/mathe_bot && git reset --hard HEAD~1 && sudo systemctl restart mathe-bot

# Update Ubuntu
sudo apt update && sudo apt upgrade -y
```

---

## 11. Notes and trade-offs

- **No domain or TLS needed.** The bot uses long-polling, so the server only makes *outbound* HTTPS to `api.telegram.org`. No inbound port besides SSH.
- **Single instance.** Telegram allows only one process per bot token. To do a zero-downtime release you'd need webhooks + a load balancer — overkill here. Brief downtime (<1s) during `systemctl restart` is fine.
- **Backups.** Hetzner snapshots are €0.01/GB/month. If you add persistence (step 9), enable **Snapshots** or daily **Backups** in the Hetzner panel.
- **Releasing the Primary IPv4 on decommission.** Hetzner bills the IPv4 *whether or not it's attached to a server*. If you ever delete the VPS, also delete the Primary IP from the **Primary IPs** tab — otherwise you keep paying ~€0.71/month for an unused address.
- **Monitoring.** A 1-line cron with `curl` to a free <https://healthchecks.io> ping is enough for hobby-scale alerting if the bot dies.

---

## Troubleshooting

| Symptom                                          | Check                                                  |
|--------------------------------------------------|--------------------------------------------------------|
| `systemctl status` shows `code=exited, status=1` | `journalctl -u mathe-bot -n 50` — usually missing env  |
| GH Action: `Permission denied (publickey)`       | private key secret incomplete; or pub key not in `~mathebot/.ssh/authorized_keys` |
| GH Action: `Host key verification failed`        | `SSH_KNOWN_HOSTS` secret wrong or missing              |
| `Conflict: terminated by other getUpdates`       | two processes running the same token — stop one        |
| `sudo: a password is required`                   | `/etc/sudoers.d/mathebot` missing or has wrong command path |
