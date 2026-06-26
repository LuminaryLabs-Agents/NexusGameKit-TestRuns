# Security

This repository is a runner harness and should not contain production secrets.

## Rules

- Store runner credentials in GitHub repository or organization secrets only.
- Do not commit Unity license data.
- Do not commit private package credentials.
- Do not commit prototype publishing credentials.
- Prefer dry-run payloads for pull request validation.
- Require explicit manual approval before publishing generated prototype output.

## RPC host safety

The runner should talk to a local or controlled Nexus Game Kit RPC host. Use an auth token for shared runner environments.
