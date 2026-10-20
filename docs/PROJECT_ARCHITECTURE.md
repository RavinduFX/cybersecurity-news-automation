# Project Architecture

## 1. Overview

The Cybersecurity News Automation project is a Python-based automation system that collects cybersecurity news from RSS feeds, prioritizes SOC-relevant articles, categorizes stories, assigns priority labels, and publishes a daily digest to Slack.

GitHub Actions handles scheduled execution and automated testing.

## 2. Architecture

```text
GitHub Actions
      |
      v
Python Environment Setup
      |
      v
Install Dependencies
      |
      v
Run Unit Tests
      |
      v
Execute news_bot.py
      |
      v
Fetch RSS Feeds
      |
      v
Parse and Normalize Articles
      |
      v
Sort by Publication Date
      |
      v
Remove Duplicate Links
      |
      v
Select Up to 10 Articles
      |
      v
Prioritize SOC-Relevant Stories
      |
      v
Categorize and Assign Priorities
      |
      v
Build Slack Digest
      |
      v
Post to Slack
```

## 3. News Sources

The bot retrieves news from:

- The Hacker News
- BleepingComputer
- Krebs on Security

Each feed is fetched using Python's `urllib.request` module and parsed using `xml.etree.ElementTree`.

If a feed cannot be retrieved or parsed, the bot logs a warning and continues with the remaining sources.

## 4. Article Processing

Each article contains the following fields:

- `source`: Name of the news source.
- `title`: Article headline.
- `link`: Article URL.
- `published`: Publication date, when available.

Articles are sorted by publication date, newest first. Articles without a valid publication date are placed after articles with valid dates.

Duplicate URLs are removed within the current execution. The bot then selects up to 10 unique articles.

## 5. SOC Relevance

The `is_soc_relevant(story)` function checks article titles against a collection of cybersecurity keywords.

Examples include:

- Vulnerabilities and CVEs
- Exploits and remote code execution
- Malware and ransomware
- Phishing and spyware
- Data breaches and credential theft
- Threat actors and intrusions
- Certificate authority compromise
- Security incidents and advisories

SOC-relevant stories are placed before other stories in the digest. The remaining stories are retained when the selected list contains them.

## 6. Categorization

The `categorize_story(story)` function assigns one category based on matching title keywords.

Supported categories:

1. Vulnerability
2. Malware & Ransomware
3. Spyware & Surveillance
4. Data Breach
5. Certificate & Trust Infrastructure
6. Threat Intelligence
7. Cyberattacks & Intrusions
8. Other

The function returns the first matching category according to the configured category order.

## 7. Priority Assignment

The `prioritize_story(story)` function assigns one of three priority levels:

- HIGH
- MEDIUM
- LOW

HIGH keywords are evaluated first, followed by MEDIUM keywords. If neither group matches, the story receives LOW priority.

Priority assignment is based on headline keyword matching rather than a full technical risk assessment.

## 8. Slack Integration

The `post_to_slack(message)` function sends the formatted digest through Slack's `chat.postMessage` API.

It reads two environment variables:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_ID`

The function checks the API response and raises an error if Slack rejects the message.

Credentials must be stored as GitHub Actions repository secrets and must never be committed to source control.

## 9. GitHub Actions

The workflow is defined in:

`.github/workflows/cybersecurity-news.yml`

It performs these tasks:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies when `requirements.txt` exists.
4. Runs unit tests.
5. Executes `news_bot.py` with the required Slack secrets.

The cron schedule is `30 3 * * *`, corresponding to 09:00 Sri Lanka Standard Time (UTC+5:30).

Manual execution is also supported through `workflow_dispatch`.

## 10. Testing

Automated tests are maintained in `tests/test_news_bot.py`.

The current test suite covers categorization, priority assignment, certificate authority compromise, SOC relevance, and general technology stories.

Tests run through Python's built-in `unittest` framework.

Run them locally with:

```bash
python -m unittest discover -s tests -v
```

## 11. Current Limitations

- Duplicate filtering does not persist between executions.
- Keyword-based classification may misclassify ambiguous headlines.
- Feed availability and publication-date formats may vary.
- The bot processes article headlines rather than performing full article content analysis.
- Slack message delivery depends on valid credentials, permissions, and API availability.

## 12. Future Improvements

Potential future enhancements include:

- Persistent duplicate filtering across daily runs.
- More precise priority scoring.
- Better handling of article publication dates and URL normalization.
- Additional trusted cybersecurity sources.
- More comprehensive automated tests.
