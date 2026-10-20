# Cybersecurity News Automation

An automated Python bot that collects cybersecurity news from trusted RSS feeds, prioritizes SOC-relevant stories, categorizes threats, and posts a daily digest to Slack using GitHub Actions.

## Features

- Fetches news from The Hacker News, BleepingComputer, and Krebs on Security.
- Removes duplicate article links within each run.
- Sorts articles by publication date.
- Prioritizes SOC-relevant stories in the daily digest.
- Categorizes articles by cybersecurity topic.
- Assigns HIGH, MEDIUM, or LOW priority labels.
- Posts the digest to a Slack channel.
- Runs automatically every day through GitHub Actions.
- Includes automated unit tests.

## News Sources

- The Hacker News
- BleepingComputer
- Krebs on Security

## Technology Stack

- Python 3.12
- RSS feeds and XML parsing
- Slack Web API
- GitHub Actions
- Python `unittest`

## How It Works

1. GitHub Actions starts the scheduled workflow.
2. Python fetches articles from the configured RSS feeds.
3. The bot parses article titles, links, sources, and publication dates.
4. Duplicate links within the current run are removed.
5. The newest articles are selected, up to the configured maximum of 10.
6. SOC-relevant stories are placed first in the digest.
7. Each story receives a category and priority label.
8. The digest is posted to Slack.

## Priority Levels

- 🔴 HIGH — potentially urgent or high-impact security stories.
- 🟡 MEDIUM — relevant security developments.
- 🟢 LOW — other stories without matching higher-priority keywords.

Priority labels are based on title keyword matching and should not be treated as a complete assessment of technical severity.

## Cybersecurity Categories

- Vulnerability
- Malware & Ransomware
- Spyware & Surveillance
- Data Breach
- Certificate & Trust Infrastructure
- Threat Intelligence
- Cyberattacks & Intrusions
- Other

## Configuration

Configure the following GitHub Actions repository secrets:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_ID`

Never commit actual tokens or credentials to the repository.

## Schedule

The GitHub Actions workflow uses the cron schedule `30 3 * * *`, which corresponds to 09:00 Sri Lanka Standard Time (UTC+5:30).

The workflow can also be triggered manually using `workflow_dispatch`.

## Run Locally

Install dependencies if a `requirements.txt` file is present:

```bash
python -m pip install -r requirements.txt
```

Set `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` in your environment, then run:

```bash
python news_bot.py
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Current Limitations

- Duplicate filtering applies only within a single execution; previously posted articles may appear again on later days.
- Categorization, SOC relevance, and priority are based on keyword matching.
- The bot depends on the availability and format of the configured RSS feeds.
- Failed feed retrievals are logged, and the bot continues processing available feeds.

## Project Documentation

- [Project Architecture](docs/PROJECT_ARCHITECTURE.md)
- [Development Log](docs/DEVELOPMENT_LOG.md)

## License

Add a license file if you intend to distribute the project as open source.
