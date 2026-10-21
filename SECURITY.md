# Security Policy

## Overview

This repository contains a Python-based cybersecurity news automation bot. It collects news from configured RSS feeds, categorizes and prioritizes stories, and delivers a daily digest to Slack through GitHub Actions.

Security issues affecting this project are taken seriously.

## Supported Versions

The latest code on the `main` branch is the primary version intended for use.

Older commits or copies may not include the latest security improvements.

## Reporting a Vulnerability

If you discover a potential security vulnerability in this project:

1. Do not publish sensitive details, access tokens, or exploitable information in a public issue.
2. Use GitHub's private vulnerability reporting feature if it is enabled for this repository.
3. If private vulnerability reporting is unavailable, contact the repository maintainer privately through an appropriate GitHub contact method.
4. Include a description of the issue, its potential impact, and steps to reproduce it when safe to do so.

Please allow the maintainer reasonable time to investigate and address a report before publicly disclosing the details.

## Security Practices

This project aims to follow these practices:

- Store Slack credentials in GitHub Actions repository secrets.
- Avoid hardcoding tokens, passwords, or other credentials in source code.
- Use HTTPS for external feed and API requests.
- Use `defusedxml` for safer XML parsing.
- Run automated Python unit tests.
- Run Bandit to identify potential Python security issues.
- Review workflow logs and security findings when failures occur.
- Grant the Slack bot only the permissions required to post messages.

These practices reduce risk but do not guarantee that the project is free of security vulnerabilities.

## Handling Secrets

The workflow expects these GitHub Actions secrets:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_ID`

Never commit their actual values to the repository or share them in public issues, screenshots, or logs.

If a token is accidentally exposed, revoke or rotate it through Slack as appropriate, update the GitHub repository secret, and review relevant workflow activity.

## Third-Party Dependencies

Python dependencies are listed in `requirements.txt`. Dependencies and GitHub Actions should be reviewed and updated when necessary to address security issues and compatibility concerns.

Bandit findings should be reviewed individually. A warning is not automatically proof of an exploitable vulnerability, and a clean scan does not guarantee complete security.

## Scope and Limitations

This project is intended for cybersecurity news aggregation and notification. It is not a security monitoring platform, incident-response service, or substitute for professional security analysis.

News categorization and priority scoring may be inaccurate or incomplete. Verify important security information against trusted sources before making operational decisions.

---

Last reviewed: October 2026
