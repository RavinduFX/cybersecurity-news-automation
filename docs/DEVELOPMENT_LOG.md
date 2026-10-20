# Development Log

## Project: Cybersecurity News Automation

A Python automation project that collects cybersecurity news, identifies SOC-relevant headlines, categorizes stories, assigns priority labels, and posts a daily digest to Slack.

## Completed Work

### 1. RSS Feed Integration

- Integrated The Hacker News RSS feed.
- Integrated BleepingComputer RSS feed.
- Integrated Krebs on Security RSS feed.
- Added error handling so one unavailable feed does not prevent processing other sources.

### 2. Article Processing

- Extracted article titles, links, source names, and publication dates.
- Added publication-date sorting.
- Added duplicate URL filtering within each execution.
- Limited each digest to a maximum of 10 articles.

### 3. Cybersecurity Categorization

Implemented keyword-based categorization for:

- Vulnerability
- Malware & Ransomware
- Spyware & Surveillance
- Data Breach
- Certificate & Trust Infrastructure
- Threat Intelligence
- Cyberattacks & Intrusions
- Other

### 4. Priority Assignment

Implemented HIGH, MEDIUM, and LOW priority labels based on configurable headline keywords.

High-priority terms include indicators such as zero-day exploitation, ransomware, remote code execution, and certificate compromise.

### 5. SOC-Relevant Story Prioritization

Added `is_soc_relevant(story)` to identify headlines associated with operational security monitoring and incident response.

Updated the digest builder to place SOC-relevant stories first while retaining other selected stories.

### 6. Slack Integration

- Integrated the Slack Web API.
- Added environment-variable configuration for the bot token and destination channel.
- Added response validation and error handling.
- Formatted stories with clickable article links, source names, categories, and priority labels.

### 7. GitHub Actions Automation

Created the scheduled workflow at:

`.github/workflows/cybersecurity-news.yml`

The workflow:

- Uses Python 3.12.
- Installs dependencies when a requirements file is available.
- Runs automated unit tests.
- Executes the news bot with GitHub Actions secrets.
- Supports manual workflow execution.
- Runs daily at 09:00 Sri Lanka Standard Time.

### 8. Automated Testing

Added unit tests covering:

- Vulnerability categorization
- Ransomware categorization
- Data breach categorization
- Spyware categorization
- Threat intelligence categorization
- Cyberattack categorization
- Unknown-story categorization
- HIGH, MEDIUM, and LOW priority assignment
- Certificate authority compromise
- SOC-relevant headlines
- General technology headlines

The latest reported test run passed all 13 tests.

## Current Project Status

The bot can fetch news from its configured RSS feeds, process and classify stories, prioritize SOC-relevant headlines, and publish the daily digest to Slack.

Scheduled execution and automated testing are configured through GitHub Actions.

## Known Limitations

- Previously posted articles can appear again on subsequent days.
- Categorization and prioritization rely on headline keywords.
- The bot does not perform full article analysis or independent vulnerability verification.
- Feed failures, network issues, and Slack API errors can affect an execution.

## Potential Next Steps

1. Add more unit tests for digest formatting and feed parsing.
2. Improve keyword matching and reduce false-positive priority assignments.
3. Consider persistent duplicate filtering if repeated stories become a problem.
4. Add more trusted cybersecurity news sources.
5. Monitor scheduled workflow runs and Slack digest quality.

## Maintenance Notes

- Keep Slack credentials in GitHub Actions secrets.
- Never commit tokens or credentials.
- Review GitHub Actions logs when a scheduled run fails.
- Run the unit tests after modifying categorization or priority logic.
