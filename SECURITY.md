# Security Policy

## Overview

The Cybersecurity News Automation Bot collects cybersecurity news from configured sources and posts news digests to a Slack channel using GitHub Actions.

Security is important because this project processes external content, uses Slack credentials, and executes automated workflows.

This document explains supported security practices, vulnerability reporting, credential handling, and the limitations of the project's security checks.

## Supported Versions

Security fixes should target the latest version on the default branch, `main`.

Older commits and branches may not receive security updates. Users should review the latest code and workflow results before running the bot.

## Reporting a Vulnerability

If you discover a potential security vulnerability in this project, please report it responsibly.

### How to report

1. Review the repository for an existing security advisory or issue describing the same problem.
2. If GitHub Private Vulnerability Reporting is enabled for this repository, use the repository's **Security** tab to submit a private vulnerability report.
3. If private reporting is unavailable, contact the repository maintainer privately through an appropriate contact method listed in their GitHub profile.

Do not publish sensitive exploit details, credentials, or information that could put users at risk in a public issue.

### Include the following information

When possible, provide:

- A clear description of the vulnerability
- The affected file, workflow, or component
- Steps to reproduce the issue
- The potential security impact
- Suggested mitigations, if known

Please allow the maintainer reasonable time to investigate and address the report before publicly disclosing technical details.

This project does not guarantee a response or resolution timeframe.

## Secrets and Credential Management

The bot may use these GitHub Actions repository secrets:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_ID`

### Required practices

- Store sensitive credentials in GitHub Actions secrets, not in source files.
- Never commit tokens, passwords, private keys, or other credentials.
- Never include secret values in README files, documentation, test fixtures, issues, pull requests, or screenshots.
- Avoid printing environment variables or credential values in workflow logs.
- Give the Slack bot only the permissions required for its intended functionality.
- Review and rotate credentials when exposure is suspected or confirmed.
- Revoke compromised credentials promptly.

The Slack channel ID is generally an identifier rather than an authentication secret, but it should still be configured through the expected secret settings for consistency.

If a credential is exposed, deleting the exposed text or commit alone is not sufficient. Revoke or rotate the credential first, then investigate the exposure.

## GitHub Actions Security

The project uses GitHub Actions to run scheduled jobs, manual runs, and pull-request checks.

The following practices should be maintained:

- Use the minimum permissions required by each workflow.
- Pin third-party actions to reviewed versions or full commit SHAs where practical.
- Review changes to workflow files before merging.
- Avoid executing untrusted pull-request code with access to secrets.
- Do not expose Slack credentials to pull-request workflows.
- Keep dependencies and GitHub Actions up to date.
- Protect the `main` branch with pull-request requirements and appropriate rules against force pushes.
- Review workflow logs when a run fails or behaves unexpectedly.

Pull-request workflows should validate changes without posting messages to the production Slack channel.

Scheduled and manually triggered runs may post to Slack. Confirm the intended branch and workflow configuration before triggering a run.

## Automated Security Checks

The repository may use the following checks, depending on the current workflow configuration.

### Unit tests

Automated tests help identify regressions in news collection, article processing, and CISA KEV matching.

Passing tests do not prove that the application is free from security vulnerabilities.

### Bandit

Bandit scans Python code for selected security-related coding patterns.

Review findings instead of automatically ignoring them. A clean scan does not guarantee secure code.

### Gitleaks

Gitleaks scans repository content for patterns that may indicate exposed credentials or other secrets.

A scan can miss secrets, and some findings may be false positives. Any suspected real credential exposure should be investigated immediately.

### CodeQL

CodeQL can analyze supported code for certain classes of security vulnerabilities.

Its findings should be reviewed and addressed where appropriate. CodeQL coverage depends on the configured workflow and analysis settings.

### Workflow failures

A successful Slack post does not necessarily mean that all tests and security checks passed. Review the overall GitHub Actions run status and the results of individual steps.

## External News and Untrusted Content

The bot collects content from external cybersecurity news sources. External titles, summaries, links, and feed content must be treated as untrusted input.

Contributors should:

- Avoid executing commands or code obtained from news feeds.
- Avoid treating article text as trusted instructions.
- Handle malformed or missing feed fields safely.
- Use reasonable network timeouts and error handling.
- Avoid logging sensitive data.
- Validate URLs and other external data where appropriate.
- Keep dependencies maintained and review dependency changes.

A news article describing an exploit does not, by itself, establish that a system is vulnerable or that exploitation has been confirmed.

## CISA Known Exploited Vulnerabilities (KEV)

The project uses a strict title-only matching rule for its CISA KEV detection.

Under this rule, a story is marked as matching the KEV catalog only when a CVE identifier found in the story title matches a CVE in the configured catalog.

A CVE appearing only in a story summary or other supplementary text must not trigger a KEV match.

This is a project-specific matching rule, not a complete vulnerability assessment. A title-only match can miss relevant vulnerabilities when a title omits the CVE identifier, and a match does not establish whether a particular system is affected.

Users should verify important vulnerability information against authoritative sources, including the official CISA KEV catalog.

## Dependency Management

Dependencies can introduce security and reliability risks.

- Review dependency changes before merging them.
- Prefer maintained packages from trusted sources.
- Investigate security advisories affecting installed dependencies.
- Upgrade vulnerable dependencies when a compatible fix is available.
- Run the relevant tests and security checks after dependency updates.

Do not assume that a dependency is secure merely because installation succeeds.

## Incident Response

If a security issue affects this project:

1. Determine the affected workflow, file, credential, or dependency.
2. Disable the affected automation if necessary to prevent further harm.
3. Revoke or rotate any exposed credentials.
4. Review GitHub Actions logs and relevant repository changes.
5. Apply and test an appropriate fix.
6. Review permissions and configuration before resuming automation.

If Slack credentials may have been exposed, prioritize credential rotation over documentation or code cleanup.

## Scope and Limitations

This policy applies to the Cybersecurity News Automation Bot and its repository-controlled application code, documentation, and GitHub Actions workflows.

It does not guarantee the security of external news providers, Slack, GitHub, third-party dependencies, or a user's wider infrastructure.

Automated scans and tests reduce certain risks but cannot guarantee that the project is free from vulnerabilities.

## Responsible Use

Use this project for legitimate cybersecurity news monitoring and awareness.

Do not use the project or its output to misrepresent vulnerability status, distribute malicious content, expose credentials, or gain unauthorized access to systems.

## Policy Updates

This policy may be updated as the project, its dependencies, and its security practices evolve.
