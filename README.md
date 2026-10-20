# Cybersecurity News Automation Bot

An automated cybersecurity news monitoring and alerting project that collects security news, assigns keyword-based priority levels and categories, and delivers a daily digest to a private Slack channel using Python and GitHub Actions.

## Project Overview

Monitoring multiple cybersecurity news sources manually can be time-consuming. This project automates the collection and presentation of security news to help readers identify potentially important security developments.

The bot retrieves news from configured sources, classifies stories using Python keyword-matching functions, formats a digest, and sends it to Slack.

## Features Implemented

- Automated cybersecurity news collection from The Hacker News, BleepingComputer, and Krebs on Security.
- Scheduled execution using GitHub Actions.
- Slack delivery to a configured private channel.
- Keyword-based news categorization.
- HIGH, MEDIUM, and LOW priority labels.
- Clickable links to original articles.
- News source attribution.
- UTC generation timestamp and total story count.
- Manual workflow execution for testing.

## News Categories

Stories are classified according to keywords in their headlines.

| Category | Purpose |
|---|---|
| 🚨 Vulnerability | CVEs, security flaws, exploits, and patches |
| 🦠 Malware & Ransomware | Malware, ransomware, trojans, rootkits, and botnets |
| 🕵️ Spyware & Surveillance | Spyware infections and surveillance-related threats |
| 🔓 Data Breach | Data leaks, exposed records, and stolen data |
| 🎯 Threat Intelligence | APTs, threat actors, and cyber-espionage indicators |
| 🛡️ Cyberattacks & Intrusions | Website compromises, hacking incidents, and intrusions |
| 📰 Other | Headlines that do not match configured category keywords |

The category assigned depends on the keywords configured in `categorize_story()` and the order in which categories are checked.

## Priority Classification

The bot assigns a priority label using the `prioritize_story()` function.

- **🔴 HIGH:** Matches configured indicators such as zero-day vulnerabilities, remote code execution, active exploitation, and ransomware.
- **🟡 MEDIUM:** Matches configured indicators such as vulnerabilities, phishing, malware, data breaches, and credential theft.
- **🟢 LOW:** Does not match the configured HIGH or MEDIUM keyword lists.

These labels are preliminary indicators based on headlines, not verified assessments of severity, exploitability, or organizational risk.

## Technology Stack

- **Python** — news processing, categorization, priority classification, and digest formatting.
- **GitHub** — source control and project hosting.
- **GitHub Actions** — scheduled automation and manual workflow runs.
- **Slack** — delivery of the cybersecurity news digest.
- **Configured news feeds and retrieval methods** — collection of articles from supported sources.

## Workflow

1. GitHub Actions starts the workflow on its configured schedule or when manually triggered.
2. The Python script retrieves stories from configured news sources.
3. The bot processes and formats the retrieved stories.
4. `categorize_story()` assigns a category based on headline keywords.
5. `prioritize_story()` assigns a preliminary priority level.
6. `build_digest()` creates the formatted digest with article links, categories, priorities, and source names.
7. The bot sends the digest to the configured Slack channel.

## Example Output

A typical Slack entry looks like this:

**🔴 HIGH · 🚨 Vulnerability · The Hacker News**

Critical FortiSIEM Flaw Gets Public Exploit PoC for Unauthenticated Remote Code Execution

The title links to the original article. The complete digest also includes a generation timestamp and total story count.

## Setup and Configuration

To run this project, you will need:

- Python installed locally if testing outside GitHub Actions.
- A GitHub repository with Actions enabled.
- A Slack app or webhook configured for message delivery.
- Access to the configured cybersecurity news sources.
- Required credentials stored securely in GitHub Actions Secrets.

### Basic setup

1. Clone the repository.
2. Install the Python dependencies specified by the project, if a dependency file is provided.
3. Configure the required GitHub Actions secrets.
4. Check the workflow configuration and scheduled execution time.
5. Run the workflow manually to verify that the digest reaches Slack.

Consult the source code and workflow configuration for the exact secret names, dependency installation commands, and schedule.

## Security Considerations

- Never commit Slack tokens, webhook URLs, or other credentials to the repository.
- Store credentials in GitHub Actions Secrets.
- Rotate any credential that is accidentally exposed.
- Review original articles and official vendor advisories before acting on alerts.
- Treat automated classifications as triage assistance rather than authoritative threat assessments.

## Current Project Status

**Implemented and tested:**

- News collection from configured sources.
- Digest formatting and Slack delivery.
- Keyword-based categorization and priority classification.
- GitHub Actions workflow execution.
- Manual test run that successfully delivered a 10-story digest with the updated categories.

## Potential Future Enhancements

- AI-generated article summaries and defensive recommendations.
- MITRE ATT&CK technique mapping.
- Duplicate-story detection and filtering.
- CVE enrichment and CVSS-based severity context.
- Weekly cybersecurity threat reports.
- Automated tests, structured logging, and failure notifications.

## Disclaimer

This project is intended for educational, defensive cybersecurity monitoring, and portfolio demonstration purposes. Automated labels are based on configured keywords and should not replace analyst review or official security advisories.
