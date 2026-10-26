# Security Policy

## Reporting a Vulnerability

Please do not disclose credentials or sensitive vulnerability details in public issues.

If private vulnerability reporting is enabled, submit a report through the repository's **Security** tab. Otherwise, contact the maintainer privately before sharing sensitive details.

Include a description, affected component, reproduction steps, and potential impact where possible.

## Credential Handling

The application uses GitHub Actions secrets for:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_ID`

Never commit real credentials to the repository. If a credential is exposed, revoke or rotate it immediately and replace the affected secret.

## Security Measures

The project uses automated tests, Bandit, and Gitleaks, alongside GitHub security features where enabled. These checks have limitations and do not guarantee that the application is vulnerability-free.

For project behavior and known limitations, see the [README](README.md).
