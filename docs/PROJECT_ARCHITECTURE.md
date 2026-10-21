# Project Architecture

## 1. Overview

Cybersecurity News Automation is a Python application that collects cybersecurity news from configured RSS feeds, categorizes headlines, assigns priority labels, prioritizes SOC-relevant stories, and sends a daily digest to Slack.

GitHub Actions provides scheduled execution, manual execution, automated testing, and security scanning.

## 2. High-Level Architecture

```text
GitHub Actions
      |
      v
Set up Python 3.12
      |
      v
Install Dependencies
      |
      v
Run Unit Tests
      |
      v
Run Bandit Security Scan
      |
      v
Execute news_bot.py
      |
      v
Fetch Configured RSS Feeds
      |
      v
Parse and Normalize Articles
      |
      v
Sort Articles and Remove
Duplicate URLs Within the Run
      |
      v
Select Up to 10 Stories
      |
      v
Evaluate SOC Relevance
      |
      v
Categorize and Assign Priorities
      |
      v
Build Digest
      |
      v
Post Digest to Slack
      |
      v
Summarize Checks and Report Failures
```

The workflow allows the news-delivery step to run after test or Bandit failures, provided the workflow has not been cancelled. A final check marks the overall workflow as failed if either quality check fails.

## 3. News Sources

The configured RSS sources are:

- [The Hacker News](https://thehackernews.com/)
- [BleepingComputer](https://www.bleepingcomputer.com/)
- [Krebs on Security](https://krebsonsecurity.com/)

The application retrieves feed data over HTTPS and parses XML using `defusedxml`.

If a feed cannot be retrieved or parsed, error handling is intended to allow processing of other sources to continue where possible.

## 4. Article Data and Processing

Articles are represented using fields such as:

- `source` — name of the news source.
- `title` — article headline.
- `link` — article URL.
- `published` — publication date, when available.

The processing pipeline sorts stories by publication date, removes duplicate URLs within the current execution, and limits the digest to a maximum of 10 stories.

Duplicate filtering is not persistent between executions.

## 5. SOC Relevance

The `is_soc_relevant(story)` function evaluates headlines against configured cybersecurity keywords.

Relevant topics may include:

- Vulnerabilities and CVEs
- Exploitation and remote code execution
- Malware and ransomware
- Phishing and spyware
- Data breaches and credential theft
- Threat actors and intrusions
- Certificate authority compromise
- Security incidents and advisories

SOC-relevant stories receive higher placement in the digest. This is keyword-based prioritization, not a replacement for professional security analysis.

## 6. Categorization

The `categorize_story(story)` function assigns a category based on configured headline keywords.

Supported categories include:

1. Vulnerability
2. Malware & Ransomware
3. Spyware & Surveillance
4. Data Breach
5. Certificate & Trust Infrastructure
6. Threat Intelligence
7. Cyberattacks & Intrusions
8. Other

The first matching category in the configured category order determines the result. Ambiguous headlines may be misclassified.

## 7. Priority Assignment

The `prioritize_story(story)` function assigns one of three priority levels:

- HIGH
- MEDIUM
- LOW

Configured headline keywords determine the assigned level. HIGH and MEDIUM indicators are checked according to the application's implemented matching rules; stories that do not meet those rules receive the default priority.

These labels help organize the digest. They do not establish the real-world severity or exploitability of a vulnerability.

## 8. Slack Integration

The application sends the formatted digest through Slack's Web API.

It requires the following environment variables:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_ID`

The GitHub Actions workflow supplies these values through repository secrets.

The Slack bot needs permission to post messages to the destination channel. The application checks the API response and handles delivery errors.

Never hardcode or commit actual credentials.

## 9. GitHub Actions Workflow

The workflow is located at:

`.github/workflows/cybersecurity-news.yml`

### Schedule

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: "30 3 * * *"
```

The cron expression runs daily at 03:30 UTC, equivalent to 09:00 Sri Lanka time.

Manual execution is available through the GitHub Actions interface.

### Workflow Steps

1. Check out the repository.
2. Set up Python 3.12.
3. Install dependencies from `requirements.txt`, when present.
4. Run unit tests using `unittest`.
5. Install Bandit.
6. Scan `news_bot.py` with Bandit.
7. Run the bot and attempt Slack delivery unless the workflow has been cancelled.
8. Summarize test and scan outcomes.
9. Mark the workflow as failed if the test suite or Bandit step fails.

The test and security-scan steps use `continue-on-error: true`, allowing subsequent steps to run. Their outcomes are evaluated at the end so failures remain visible in the overall workflow status.

## 10. Dependencies and Testing

The project dependency is documented in `requirements.txt`:

```text
defusedxml>=0.7.1,<1.0
```

The tests are located at:

`tests/test_news_bot.py`

Run the suite locally with:

```bash
python -m unittest discover -s tests -v
```

Bandit is installed by the workflow and scans `news_bot.py` using:

```bash
python -m bandit -r news_bot.py -ll
```

Review scan findings individually. A warning is not automatically proof of an exploitable issue, and a clean scan does not guarantee complete security.

## 11. Security Considerations

- Keep Slack credentials in GitHub Actions secrets.
- Use HTTPS for external requests.
- Parse RSS XML using `defusedxml`.
- Review dependency and workflow updates.
- Inspect failed test and security-scan logs.
- Give the Slack bot only the required permissions.

See `SECURITY.md` for the project's security policy.

## 12. Limitations

- Duplicate filtering does not persist across executions.
- Categorization and priority scoring rely on headline keywords.
- Feed formats and availability can vary.
- Headlines are not a substitute for full article or vulnerability analysis.
- Slack delivery depends on credentials, permissions, network connectivity, and API availability.
- Automated tests and security scans cannot guarantee defect-free or secure software.

## 13. Potential Improvements

- Persistent duplicate detection.
- Better publication-date handling and URL normalization.
- More precise categorization and priority scoring.
- Additional trusted news sources.
- Expanded unit and integration tests.
- Improved monitoring of feed failures and Slack delivery.

---

Last updated: October 2026
