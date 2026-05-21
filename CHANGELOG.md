# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `CHANGELOG.md` (this file).
- `CLAUDE.md` for future Claude Code sessions.
- `DEPLOY.md` with Hetzner VPS + SSH + systemd setup instructions.
- `deploy/mathe-bot.service` — systemd unit file for running the bot in production.
- `.github/workflows/deploy.yml` — CI/CD pipeline (syntax check + SSH deploy on push to `main`).

### Changed
- Excluded `DEPLOY.TASK.md` (one-off task notes) from version control.
- Added CI status badge to the README.
- Trimmed `CLAUDE.md` — removed architecture notes that are derivable from the code itself.

## [0.2.0] — 2026-04-24

### Fixed
- Percentage calculation bug in grade 6 tasks.

### Added
- Hints (💡 button) on every task.
- Explanations shown after each answer.

## [0.1.0] — 2026-04-24

### Added
- Initial release of the Mathe-Quiz Telegram bot.
- Grades 5–9 with topic-specific generators (arithmetic, fractions, percentages, geometry, equations, quadratics, probability, sequences, etc.).
- Knobelaufgaben (brain teasers).
- Difficulty selection: leicht / mittel / schwer / zufällig.
- Daily challenge (`/tagesaufgabe`) seeded by date so all users get the same task.
- Per-grade score tracking via `ctx.user_data`.
- German-only UI strings centralised in `messages.py`.
