# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

German-language Telegram bot that generates math quizzes for grades 5–9 plus brain teasers (Knobelaufgaben). Python 3, `python-telegram-bot` (async), no database — all state lives in `ctx.user_data` per chat.

## Commands

```bash
pip install -r requirements.txt    # install deps
cp .env.example .env               # then put TELEGRAM_BOT_TOKEN=... inside
python3 bot.py                     # run (long-polling)
```

No test suite, no linter, no build step. Verifying changes means running the bot and exercising the affected flow in Telegram.

## German UI convention

The bot is German-facing (B1–B2). Keep all user-visible strings in `messages.py` or inline German in task `question`/`hint`/`explanation`. Code identifiers, comments, and topic keys stay English. Slash commands have both German and English aliases (`/hilfe` + `/help`, `/punkte`, `/zuruecksetzen` + `/reset`, `/tagesaufgabe` + `/daily`) — preserve both when adding commands.

## Changelog discipline

**Every commit must update `CHANGELOG.md` in the same commit** (not a follow-up). The repo uses [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — new entries go under the `## [Unreleased]` section at the top, grouped by `Added` / `Changed` / `Fixed` / `Removed` / `Deprecated` / `Security`.

- Phrase entries from the user's perspective ("Added Tagesaufgabe button", not "Refactored `cmd_daily`").
- Skip the changelog only for purely mechanical commits that change nothing observable (typo fixes in comments, formatting). When in doubt, add an entry — it's cheap.
- Cutting a release: rename `## [Unreleased]` → `## [X.Y.Z] — YYYY-MM-DD`, then add a fresh empty `## [Unreleased]` block above it. Tag the commit with `vX.Y.Z`.
- Version bumps follow [SemVer](https://semver.org/): breaking user-facing change → major, new feature → minor, fix → patch.

## GitHub access

The `origin` remote uses **SSH** (`git@github.com:Alexsonya/mathe_bot.git`), authenticated by `~/.ssh/id_ed25519`. Plain `git push origin main` works without prompts. Do not switch the remote back to HTTPS — no credential helper is configured, and the cached `gh` CLI token is expired (`gh auth status` fails). HTTPS pushes will hang on the username prompt.

- If a future task needs `gh pr` / `gh issue` / `gh run`, run `gh auth login` first; everything `git`-native works as-is.
- The CI/CD deploy key for GitHub Actions (DEPLOY.md §8a) must be a **separate** passphrase-less key — don't paste `~/.ssh/id_ed25519` into Actions secrets.

## Deployment

Production deployment is documented in `DEPLOY.md` (Hetzner VPS + `systemd`). CI/CD lives in `.github/workflows/deploy.yml` and redeploys on every push to `main`. The systemd unit shipped at `deploy/mathe-bot.service` is the source of truth — if you change paths or env vars, update the unit and DEPLOY.md together.
