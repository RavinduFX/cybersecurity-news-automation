# Cybersecurity News Automation Bot

An automated cybersecurity news bot that collects articles from trusted cybersecurity news sources, identifies relevant vulnerability information, and posts a daily digest to Slack using GitHub Actions.

## Features

- Automatically collects cybersecurity news from configured RSS feeds.
- Currently configured sources:
  - The Hacker News
  - BleepingComputer
  - Krebs on Security
- Posts a formatted news digest to a configured Slack channel.
- Supports manual execution through GitHub Actions.
- Runs automated unit tests.
- Uses Bandit to scan Python code for common security issues.
- Uses GitHub Actions to automate checks and scheduled execution.
- Supports strict, title-only CISA Known Exploited Vulnerabilities (KEV) matching.
- Includes secret scanning and CodeQL analysis when those workflows are enabled.

## How It Works

1. GitHub Actions starts the workflow on its scheduled run or when manually triggered.
2. The workflow checks out the repository.
3. Python is configured and project dependencies are installed.
4. Automated unit tests run.
5. Bandit scans the Python bot code.
6. The bot fetches and processes cybersecurity news.
7. The formatted digest is posted to Slack.
8. The workflow reports the quality-check results and fails if the tests or Bandit scan failed.

**Important:** The workflow can post the Slack digest successfully and still finish with a failed status if automated tests or the security scan fail. A successful Slack message does not mean every check passed.

## News Sources

The bot currently uses these sources:

- [The Hacker News](https://thehackernews.com/)
- [BleepingComputer](https://www.bleepingcomputer.com/)
- [Krebs on Security](https://krebsonsecurity.com/)

News availability and feed content depend on the respective publishers.

## Automated Schedule

The `Daily Cybersecurity News` workflow is scheduled with this GitHub Actions cron expression:

`30 3 * * *`

GitHub Actions cron schedules use UTC. This schedule corresponds to **03:30 UTC every day**, or **09:00 Sri Lanka Standard Time (UTC+5:30)**.

GitHub-hosted scheduled workflows can occasionally be delayed. They are not guaranteed to start at the exact scheduled minute.

You can also start a run manually:

1. Open the repository on GitHub.
2. Select **Actions**.
3. Select **Daily Cybersecurity News**.
4. Click **Run workflow**.
5. Select the target branch if prompted.
6. Click **Run workflow** to start the job.

## Required GitHub Secrets

The bot requires these repository secrets:

| Secret name | Purpose |
| --- | --- |
| `SLACK_BOT_TOKEN` | Authenticates the Slack bot |
| `SLACK_CHANNEL_ID` | Identifies the Slack channel that receives the digest |

Configure secrets under:

**Repository → Settings → Secrets and variables → Actions**

Add each secret using the exact name shown above.

Never commit secret values to the repository or include them in screenshots, logs, issues, or documentation. If a token is exposed, revoke or rotate it promptly.

The Slack bot must have the appropriate permissions to post messages to the target channel and must be added to the channel when required.

## Automated Tests

The workflow runs the unit tests using:

`python -m unittest discover -s tests -v`

The tests are stored in the `tests/` directory.

They help verify expected behavior, including strict CVE matching for KEV detection.

### Understanding test results

- **Passed:** The tests completed successfully.
- **Failed:** One or more tests need investigation.
- **Skipped or not run:** Check the workflow logs to determine why the step did not execute.

A successful Slack delivery is not a replacement for passing unit tests.

## Python Security Scan

The workflow uses Bandit to scan `news_bot.py`:

`python -m bandit -r news_bot.py -ll`

Bandit identifies certain common security issues in Python code. Review its findings to determine whether a change is needed.

A clean Bandit result does not guarantee that the entire application is free of vulnerabilities.

## CISA Known Exploited Vulnerabilities (KEV)

The bot uses a strict **title-only CVE matching policy** to decide whether a story qualifies for a KEV label.

A story qualifies only when:

1. Its title contains a CVE identifier.
2. That identifier matches a CVE in the CISA KEV catalog used by the bot.

The following do not qualify on their own:

- A CVE identifier appearing only in the article summary.
- A summary mentioning that CISA added vulnerabilities to the KEV catalog without a matching CVE in the title.
- A vulnerability described as exploited without a title CVE that matches the catalog.

**A missing KEV label does not prove that a vulnerability is not exploited.** It means the story did not meet the project's strict matching rule.

## Pull Requests and Branch Protection

The repository uses a protected `main` branch and a pull-request workflow.

When the `Daily Cybersecurity News` workflow runs for a pull request targeting `main`, it performs the quality checks but skips the Slack-posting step. This prevents test runs from sending unintended digests to the production Slack channel.

Recommended repository protections include:

- Require pull requests before merging.
- Require appropriate status checks to pass before merging.
- Block force pushes to `main`.

If required status checks are configured, select the actual check names reported by GitHub Actions. Confirm that the checks have completed successfully before merging.

## Troubleshooting

### The Slack digest was posted, but the workflow failed

The workflow allows the test and Bandit steps to continue after a failure so that the news-posting step can still run. A final step then marks the workflow as failed if either check failed.

To investigate:

1. Open the repository's **Actions** tab.
2. Select the affected `Daily Cybersecurity News` run.
3. Open **Run automated tests** and review the output.
4. Open **Run Python security scan** and review any findings.
5. Open the final workflow step to see which check caused the failure.
6. Fix the underlying issue and rerun the workflow.

### No Slack message was received

Check the following:

- The workflow completed the news-posting step.
- `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` exist in repository Actions secrets.
- The token is valid and has the required permissions.
- The bot can post to the target Slack channel.
- The workflow logs do not contain Slack API or network errors.

Never share the token while troubleshooting.

### No KEV label appeared

Check whether the article title contains a CVE identifier that matches the CISA KEV catalog. Under the current policy, a CVE appearing only in the summary is insufficient.

### The scheduled workflow did not run at the expected time

Check the **Actions** tab, confirm the workflow is enabled, and allow for possible GitHub Actions scheduling delays. Use **Run workflow** to trigger a manual run when needed.

### Secret scanning or CodeQL reports a problem

Open the corresponding workflow run and review the failing step. Investigate the finding and follow the recommended remediation. Do not publish credentials or sensitive details while reporting the issue.

## Repository Structure

The main project files include:

- `news_bot.py` — news collection, processing, and Slack delivery logic.
- `tests/test_news_bot.py` — automated unit tests.
- `requirements.txt` — project dependencies, if present.
- `.github/workflows/cybersecurity-news.yml` — scheduled news workflow and quality checks.
- `.github/workflows/gitleaks.yml` — secret-scanning workflow, if present.
- Other GitHub Actions workflows — additional configured checks, such as CodeQL, if present.

The repository contents may evolve as the project is improved.

## Security Best Practices

- Keep all credentials in GitHub Actions secrets.
- Review test and security scan failures instead of ignoring them.
- Use pull requests to introduce changes to `main`.
- Review workflow permissions before adding new actions.
- Pin third-party GitHub Actions to trusted versions or commit SHAs.
- Keep project dependencies reasonably up to date.
- Treat news articles as information sources, not as instructions to execute commands.
- Do not claim a vulnerability is confirmed in CISA KEV unless it meets the project's matching criteria.

## Limitations

- News availability depends on external RSS feeds and publisher availability.
- Scheduled GitHub Actions runs can be delayed.
- Bandit and automated tests cannot detect every possible defect.
- KEV labels depend on the CVE information in article titles and the catalog data available to the bot.
- Successful delivery does not guarantee that all quality checks passed.

## License

If this repository includes a `LICENSE` file, refer to it for the applicable license terms. Otherwise, no specific open-source license should be assumed.
