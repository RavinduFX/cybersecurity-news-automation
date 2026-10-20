# Cybersecurity News Automation Bot

An automated cybersecurity news digest that collects security news and delivers categorized, priority-labelled stories to a private Slack channel using Python and GitHub Actions.

## Project Overview

The Cybersecurity News Automation Bot reduces the effort required to monitor cybersecurity news by collecting stories from multiple security news sources and publishing a daily digest to Slack.

The project demonstrates practical skills in Python automation, API/webhook integration, GitHub Actions, security news monitoring, and basic threat prioritization.

## Features Implemented

- **Automated news collection** from The Hacker News, BleepingComputer, and Krebs on Security.
- **Daily scheduled execution** using GitHub Actions.
- **Slack integration** to deliver a formatted news digest to a private channel.
- **Story categorization** using title-based keyword matching.
- **Priority classification** into HIGH, MEDIUM, and LOW.
- **Clickable article links** and source attribution.
- **UTC generation timestamps** and total story counts.

## News Categories

The bot currently classifies stories into these categories:

| Category | Purpose |
|---|---|
| Vulnerability | Security flaws, CVEs, exploits, and patches |
| Malware & Ransomware | Malware, ransomware, trojans, rootkits, and botnets |
| Spyware & Surveillance | Spyware infections and surveillance-related threats |
| Data Breach | Data leaks, exposed records, and stolen data |
| Threat Intelligence | Threat actors, APTs, and cyber-espionage indicators |
| Cyberattacks & Intrusions | Website compromises, hacking incidents, and intrusions |
| Other | Stories that do not match the configured keywords |

## Priority Classification

- **HIGH:** Headlines containing configured indicators such as zero-day exploits, remote code execution, ransomware, and active exploitation.
- **MEDIUM:** Headlines containing indicators such as vulnerabilities, phishing, malware, data breaches, and credential theft.
- **LOW:** Headlines that do not match the configured HIGH or MEDIUM keywords.

Priority labels are preliminary, keyword-based signals. They are not a definitive assessment of the actual severity or exploitability of a threat.

## Technology Stack

- Python
- GitHub
- GitHub Actions
- Slack incoming webhook or configured Slack integration
- RSS feeds and/or the configured news-source retrieval methods

## Workflow

1. GitHub Actions starts the bot on its configured schedule.
2. The Python script retrieves cybersecurity news from configured sources.
3. The bot processes and formats the collected stories.
4. Each story receives a category and priority label based on its headline.
5. The bot publishes the daily digest to the configured Slack channel.

## Security Considerations

- Store Slack credentials and other secrets in GitHub Actions Secrets.
- Never commit tokens, passwords, or webhook URLs to the repository.
- Rotate credentials immediately if they are accidentally exposed.
- Review source articles before acting on automated classifications.
- Use official vendor advisories to validate vulnerability and remediation details.

## Current Project Status

**Implemented and tested:** News collection, digest formatting, keyword-based categorization, priority labelling, Slack delivery, and GitHub Actions execution.

The latest manual workflow run successfully delivered a 10-story digest to Slack with the updated Spyware & Surveillance and Cyberattacks & Intrusions categories.

## Potential Future Enhancements

- Add AI-generated article summaries and recommended defensive actions.
- Map relevant stories to MITRE ATT&CK techniques.
- Detect duplicate stories across news sources.
- Improve severity assessment using source details and CVSS data where available.
- Generate weekly cybersecurity threat reports.
- Add automated tests, logging, and error notifications.

## Disclaimer

This project is intended for educational, defensive cybersecurity monitoring, and portfolio demonstration purposes. Automated categories and priorities are indicative only and should not replace analyst validation.
