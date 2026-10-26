# Cybersecurity News Automation Bot

A Python automation project that collects cybersecurity news from RSS feeds, checks article titles against the CISA Known Exploited Vulnerabilities (KEV) catalog, and delivers a digest to Slack using GitHub Actions.

## Features

- Automated news collection from The Hacker News, BleepingComputer, and Krebs on Security.
- Slack notifications for cybersecurity news.
- Title-based CVE matching against the CISA KEV catalog.
- Scheduled and manual execution with GitHub Actions.
- Unit testing with Python `unittest`.
- Static security analysis using Bandit and secret scanning using Gitleaks.

## Technology Stack

Python 3.12 · GitHub Actions · Slack API · RSS · Bandit · Gitleaks

## Configuration

Add the following under **GitHub → Settings → Secrets and variables → Actions**:

| Secret | Purpose |
|---|---|
| `SLACK_BOT_TOKEN` | Slack authentication |
| `SLACK_CHANNEL_ID` | Destination Slack channel |

Never commit credentials or tokens to source control.

## Running the Workflow

1. Open the repository's **Actions** tab.
2. Select **Daily Cybersecurity News**.
3. Click **Run workflow**, if available.

The scheduled workflow runs at 03:30 UTC (09:00 Sri Lanka Standard Time).

## Tests

Run the unit tests locally with:

```bash
python -m unittest discover -s tests -v
```

Tests are located in `tests/test_news_bot.py`.

## Limitations

KEV matching currently checks article titles only. A match does not confirm that a particular system is vulnerable. Automated tests and security scanners cannot guarantee the absence of vulnerabilities.

## Repository Structure

```text
.github/
├── workflows/
│   ├── cybersecurity-news.yml
│   └── gitleaks.yml
tests/
└── test_news_bot.py
docs/
├── ARCHITECTURE.md
└── DEVELOPMENT-LOG.md
news_bot.py
requirements.txt
README.md
SECURITY.md
```

## Documentation

- [Architecture](docs/PROJECT_ARCHITECTURE.md)
- [Development Log](docs/DEVELOPMENT_LOG.md)
- [Security Policy](SECURITY.md)

## Repository

[View the project on GitHub](https://github.com/RavinduFX/cybersecurity-news-automation)
