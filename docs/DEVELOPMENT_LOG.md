# Development Log

## Project

**Name:** Cybersecurity News Automation Bot

**Repository:** https://github.com/RavinduFX/cybersecurity-news-automation

**Default branch:** `main`

## Purpose

This project automates the collection of cybersecurity news and delivers a digest to a configured Slack channel using GitHub Actions.

This log records significant project changes, testing milestones, maintenance work, and known limitations.

## Development History

### Milestone 1 — Initial Automation

**Status:** Implemented

- Established the cybersecurity news automation project.
- Configured news collection from The Hacker News, BleepingComputer, and Krebs on Security.
- Configured Slack delivery using GitHub Actions secrets.
- Added scheduled and manual workflow execution.

### Milestone 2 — Automated Testing

**Status:** Implemented; verify against the latest workflow run

- Added automated Python unit tests under `tests/`.
- Configured GitHub Actions to run the test suite.
- Added test execution results to the workflow logs.

**Verification:** Check the latest GitHub Actions run to confirm the current test status.

### Milestone 3 — Python Security Scanning

**Status:** Configured; verify against the latest workflow run

- Added Bandit scanning for `news_bot.py`.
- Configured the workflow to report test and security-scan outcomes.
- Added a final workflow step that fails the run if the tests or Bandit scan fail.

A successful Slack post does not necessarily mean all quality checks passed.

### Milestone 4 — Repository Security

**Status:** Configured; verify the current repository settings

- Added a Gitleaks workflow for secret scanning.
- Configured CodeQL analysis.
- Established branch protection rules for `main`.

Review the repository's current workflow files and branch rules to confirm which protections are active.

### Milestone 5 — Strict CISA KEV Detection

**Status:** Implemented; verify with automated tests

- Defined title-only matching for CISA Known Exploited Vulnerabilities (KEV).
- Added tests for CVE matches in titles.
- Added tests to ensure summary-only matches do not trigger a KEV label.
- Added tests for CVEs absent from the catalog and empty catalogs.

**Expected behavior:** A story is marked as a KEV match only when a CVE identifier in its title matches an identifier in the configured KEV catalog.

This rule can miss relevant vulnerabilities when their titles omit CVE identifiers. A match does not prove that a particular system is affected.

### Milestone 6 — Documentation

**Status:** In progress

Documentation includes or is planned to include:

- `README.md` — project overview and setup instructions
- `CONTRIBUTING.md` — contribution guidelines
- `SECURITY.md` — security policy
- `docs/DEVELOPMENT-LOG.md` — development history
- `docs/ARCHITECTURE.md` — system design and data flow

Update this section when documentation changes have been committed.

## Current Workflow

The scheduled workflow is configured with:

`30 3 * * *`

This corresponds to 03:30 UTC, or 09:00 in Sri Lanka Standard Time (UTC+05:30).

GitHub Actions scheduling is not guaranteed to start at the exact minute.

The workflow also supports manual execution and pull-request checks. Pull-request runs are configured to skip production Slack posting.

## Known Limitations

- News availability and quality depend on external feeds.
- External feeds can be unavailable, malformed, delayed, or changed.
- Scheduled execution can be delayed by GitHub Actions.
- Slack delivery depends on valid credentials, permissions, and network availability.
- Automated tests and security scanners cannot guarantee the absence of bugs or vulnerabilities.
- Title-only KEV matching can miss CVEs that do not appear in article titles.
- A successful notification does not independently verify the accuracy of every article.

## Maintenance Checklist

- [ ] Review recent GitHub Actions results.
- [ ] Investigate failed tests and security scans.
- [ ] Review dependency and workflow updates.
- [ ] Confirm Slack secrets remain valid and are not exposed.
- [ ] Update documentation when application behavior changes.
- [ ] Record significant changes in this log.

## How to Update This Log

Add a dated entry for significant changes. Include:

- Date
- Change made
- Reason for the change
- Tests or security checks performed
- Outcome and any known limitations

Do not record secret values, private credentials, or sensitive incident details in this document.
