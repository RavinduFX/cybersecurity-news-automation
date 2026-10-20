# Cybersecurity News Automation Bot

An automated cybersecurity news monitoring and alerting project that collects security news, assigns keyword-based priority levels and categories, and delivers a daily digest to a private Slack channel using Python and GitHub Actions.

**Project status:** Working prototype — the GitHub Actions workflow has been manually tested, and the bot successfully delivered a 10-story cybersecurity news digest to Slack.

**Repository:** [RavinduFX/cybersecurity-news-automation](https://github.com/RavinduFX/cybersecurity-news-automation)

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [News Categories](#news-categories)
- [Priority Classification](#priority-classification)
- [Technology Stack](#technology-stack)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Setup and Configuration](#setup-and-configuration)
- [Security Considerations](#security-considerations)
- [Current Project Status](#current-project-status)
- [Future Enhancements](#future-enhancements)
- [Disclaimer](#disclaimer)

## Project Overview

Monitoring multiple cybersecurity news sources manually can be time-consuming. This project automates the collection and presentation of security news to help readers identify potentially important security developments.

The bot retrieves news from configured sources, classifies stories using Python keyword-matching functions, formats a digest, and sends it to a private Slack channel.

The project demonstrates practical skills in Python automation, GitHub Actions, Slack integration, news monitoring, and basic security-event triage.

## Features

- **Automated news collection** from The Hacker News, BleepingComputer, and Krebs on Security.
- **Scheduled execution** using GitHub Actions.
- **Slack integration** to deliver a formatted daily digest.
- **Keyword-based categorization** of cybersecurity news.
- **Priority classification** into HIGH, MEDIUM, and LOW.
- **Clickable article links** to original news sources.
- **Source attribution** for every story.
- **UTC generation timestamp** and total story count.
- **Manual workflow execution** for testing and troubleshooting.

## News Categories

Stories are categorized using keywords found in their headlines.

| Category | Purpose |
|---|---|
| 🚨 Vulnerability | CVEs, security flaws, exploits, and patches |
| 🦠 Malware & Ransomware | Malware, ransomware, trojans, rootkits, and botnets |
| 🕵️ Spyware & Surveillance | Spyware infections and surveillance-related threats |
| 🔓 Data Breach | Data leaks, exposed records, and stolen data |
| 🎯 Threat Intelligence | APTs, threat actors, and cyber-espionage indicators |
| 🛡️ Cyberattacks & Intrusions | Website compromises, hacking incidents, and intrusions |
| 📰 Other | Headlines that do not match configured category keywords |

The `categorize_story()` function assigns a category based on the configured keywords and their order in the code. A headline that matches multiple categories receives the first matching category.

## Priority Classification

The `prioritize_story()` function assigns a preliminary priority level based on keywords in each headline.

- **🔴 HIGH:** Indicators such as zero-day vulnerabilities, remote code execution, active exploitation, ransomware, and MFA bypass.
- **🟡 MEDIUM:** Indicators such as vulnerabilities, phishing, malware, data breaches, credential theft, and privilege escalation.
- **🟢 LOW:** Headlines that do not match the configured HIGH or MEDIUM keyword lists.

These labels are intended to support initial triage. They do not independently establish the actual severity, exploitability, or business impact of a threat.

## Technology Stack

- **Python** — news processing, categorization, priority classification, and digest formatting.
- **GitHub** — source control and project hosting.
- **GitHub Actions** — scheduled automation and manual workflow execution.
- **Slack** — delivery of the cybersecurity news digest.
- **Configured news feeds and retrieval methods** — collection of articles from supported sources.

## How It Works

1. GitHub Actions starts the workflow according to its configured schedule or a manual trigger.
2. The Python script retrieves stories from configured cybersecurity news sources.
3. The bot processes the collected stories.
4. `categorize_story()` assigns a category using headline keywords.
5. `prioritize_story()` assigns a preliminary priority level.
6. `build_digest()` formats the stories with their links, categories, priorities, and sources.
7. The bot sends the formatted digest to the configured Slack channel.

## Example Output

A typical Slack entry looks like this:

**🔴 HIGH · 🚨 Vulnerability · The Hacker News**

Critical FortiSIEM Flaw Gets Public Exploit PoC for Unauthenticated Remote Code Execution

The headline links to the original article. The complete digest includes a generation timestamp, multiple categorized stories, and a total story count.

## Setup and Configuration

### Prerequisites

- A GitHub account and repository with GitHub Actions enabled.
- Python installed locally if you want to run or test the bot outside GitHub Actions.
- A Slack app or incoming webhook configured for message delivery.
- Access to the configured cybersecurity news sources.
- The required credentials stored securely in GitHub Actions Secrets.

### Basic Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/RavinduFX/cybersecurity-news-automation.git
   ```

2. Open the project directory:

   ```bash
   cd cybersecurity-news-automation
   ```

3. Review the Python script and GitHub Actions workflow.

4. Install the dependencies specified by the project, if a dependency file is provided.

5. Configure the required GitHub Actions secrets using the names expected by the workflow.

6. Check the workflow schedule and configured time zone.

7. Open the **Actions** tab in GitHub and manually run the workflow to verify that the digest reaches Slack.

Refer to the actual source code and workflow configuration for the exact dependency installation commands, secret names, and scheduling details.

## Security Considerations

- Never commit Slack bot tokens, webhook URLs, passwords, or other credentials to the repository.
- Store required credentials in GitHub Actions Secrets.
- Rotate any credential that is accidentally exposed.
- Review original articles and official vendor advisories before acting on automated alerts.
- Treat keyword-based classifications as triage assistance rather than authoritative threat assessments.
- Review external links and news content before using them in security investigations.

## Current Project Status

### Implemented and Tested

- News collection from configured sources.
- Formatted cybersecurity digest generation.
- Keyword-based story categorization.
- HIGH, MEDIUM, and LOW priority classification.
- Slack message delivery.
- GitHub Actions workflow execution.
- Manual test run that successfully delivered a 10-story digest with the updated categories.

The project currently uses headline-based keyword matching. More advanced threat enrichment and automated article summarization remain potential future enhancements.

## Future Enhancements

- **AI-generated summaries:** Explain what happened and why a story matters to security teams.
- **Defensive recommendations:** Suggest practical investigation and mitigation steps based on verified article content.
- **MITRE ATT&CK mapping:** Associate relevant stories with applicable tactics and techniques.
- **Duplicate detection:** Reduce repeated stories across multiple news sources.
- **CVE enrichment:** Include verified vulnerability identifiers and CVSS information when available.
- **Weekly threat reports:** Summarize recurring threats and significant developments.
- **Automated testing:** Add unit tests for categorization, priority classification, and digest formatting.
- **Logging and error notifications:** Improve troubleshooting and workflow reliability.

## Disclaimer

This project is intended for educational, defensive cybersecurity monitoring, and portfolio demonstration purposes. Automated categories and priority labels are based on configured keywords and should not replace analyst review, official security advisories, or a formal risk assessment.
