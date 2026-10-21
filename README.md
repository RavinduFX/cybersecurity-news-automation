# Cybersecurity News Automation

An automated Python bot that collects cybersecurity news from trusted RSS feeds, prioritizes relevant stories, categorizes them, and delivers a daily digest to Slack using GitHub Actions.

## Features

- **Automated daily delivery:** Runs on a scheduled GitHub Actions workflow.
- **Multiple news sources:** Collects articles from:
  - [The Hacker News](https://thehackernews.com/)
  - [BleepingComputer](https://www.bleepingcomputer.com/)
  - [Krebs on Security](https://krebsonsecurity.com/)
- **Story categorization:** Groups articles into cybersecurity categories, including vulnerabilities, cyberattacks, malware and ransomware, data breaches, certificate and trust infrastructure, and threat intelligence.
- **Priority scoring:** Helps surface high-priority cybersecurity stories.
- **SOC relevance filtering:** Identifies stories that may be useful for Security Operations Center (SOC) monitoring and analysis.
- **Slack notifications:** Sends the daily digest to a configured Slack channel.
- **Automated quality checks:** Includes Python unit tests and Bandit security analysis in the GitHub Actions workflow.

## How it works

1. GitHub Actions starts the scheduled workflow.
2. The Python bot fetches articles from the configured RSS feeds.
3. Stories are categorized, assessed for priority, and evaluated for SOC relevance.
4. The bot prepares a digest containing up to 10 stories.
5. The digest is sent to the configured Slack channel.
6. Automated tests and security checks run as defined in the workflow.

## Project structure

```text
cybersecurity-news-automation/
├── news_bot.py
├── requirements.txt
├── tests/
│   └── test_news_bot.py
├── .github/
│   └── workflows/
│       └── cybersecurity-news.yml
└── README.md
```

## Requirements

- A GitHub repository
- A Slack workspace and destination channel
- A Slack bot token with permission to post messages to the selected channel
- Python and the dependencies listed in `requirements.txt`

The scheduled automation runs through GitHub Actions, so you do not need to keep your own computer running.

## Configuration

### 1. Configure GitHub Secrets

In your repository, open **Settings → Secrets and variables → Actions** and add these repository secrets:

| Secret name | Purpose |
|---|---|
| `SLACK_BOT_TOKEN` | Authenticates the Slack bot |
| `SLACK_CHANNEL_ID` | Identifies the Slack channel that receives the digest |

Use the actual secret values in GitHub's secret fields. Never paste tokens or other credentials into source code, documentation, issues, or commit messages.

The Slack bot must have permission to post messages to the destination channel.

### 2. Install Python dependencies

The `requirements.txt` file should contain:

```text
defusedxml>=0.7.1,<1.0
```

This dependency provides safer XML parsing for RSS feeds.

### 3. Configure the schedule

The workflow uses this cron expression for the daily run:

```yaml
- cron: '30 3 * * *'
```

GitHub Actions interprets cron schedules in UTC. This corresponds to **03:30 UTC, or 9:00 AM Sri Lanka time**.

Scheduled workflows can occasionally start later than the requested time because of GitHub Actions scheduling load.

## Testing and security checks

The project includes unit tests in `tests/test_news_bot.py` to verify story categorization, priority handling, and SOC relevance logic.

The GitHub Actions workflow also runs Bandit to check Python code for common security issues.

Check the individual step results in the **Actions** tab. If a step is configured with `continue-on-error: true`, a failed check may not prevent later workflow steps from running. A successful Slack delivery therefore does not, by itself, prove every quality check passed.

## Troubleshooting

### No Slack digest received

1. Open the repository's **Actions** tab.
2. Open the latest workflow run.
3. Review the logs for the news collection and Slack posting steps.
4. Confirm that `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` exist under repository Actions secrets.
5. Verify that the bot can post to the selected Slack channel.

### Workflow fails during dependency installation

Confirm that `requirements.txt` exists at the repository root and contains the required dependencies.

### Tests fail

Open the failed test step and identify the failing test before changing the code. Update the relevant logic and tests together, then rerun the workflow.

### No new stories appear

RSS feeds can be temporarily unavailable or may not publish new articles. Check the workflow logs before assuming the Slack integration is broken.

## Security considerations

- Keep Slack credentials in GitHub Secrets.
- Use HTTPS for external feed and API requests.
- Parse RSS XML using `defusedxml`.
- Review test and Bandit results regularly.
- Give the Slack bot only the permissions it needs.
- Avoid logging credentials or sensitive information.

## Cost

The project is designed to run with GitHub Actions and Slack without requiring a paid news API or a separate always-on server. Actual costs and usage limits depend on your GitHub plan, repository visibility, and any services you choose to add.

## Current status

The project has passed its latest reported GitHub Actions test run, and the Slack digest has been received successfully. Continue checking future scheduled runs to confirm ongoing reliability.

## Future improvements

Potential enhancements include:

- Better filtering of duplicate stories
- More precise vulnerability and threat-intelligence classification
- Improved reporting of failed RSS feeds
- More detailed monitoring of workflow health
- Additional trusted cybersecurity news sources

---

**Built with Python, RSS, Slack, and GitHub Actions.**
