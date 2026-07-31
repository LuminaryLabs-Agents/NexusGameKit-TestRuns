# Security

This repository is an external validation harness for Nexus Game Kit. It must not contain production secrets.

## Handling sensitive information

- Do not commit runner tokens, Unity license data, private package credentials, or prototype-publishing credentials.
- Store workflow credentials in GitHub repository or organization secrets, not in tracked configuration, payloads, or documentation.
- Treat generated reports and workflow artifacts as potentially sensitive: they can contain submitted payloads and RPC responses. Review them before sharing or retaining them outside the project.
- Prefer dry-run payloads for pull-request validation. Local payload validation is useful, but it is not an authorization or access-control boundary.

## RPC host safety

- Connect the runner only to a local or controlled Nexus Game Kit RPC host.
- The client accepts an RPC URL and optional token through command-line options or environment variables. It adds the `X-Nexus-Token` request header only when a token is configured; it does not require a token by itself.
- Shared runner environments should require host-side authentication and restrict network access to the RPC host.

## Live execution and publishing

- The tracked live-host workflow is manually dispatched and reads its token from a GitHub secret.
- Require explicit manual approval before publishing generated prototype output.
- Preserve validation, queue-execution, and report artifacts for failures so the event can be investigated without rerunning unsafe work.

## Reporting a vulnerability

A repository-local security contact, disclosure process, and response timeline are not currently documented. Coordinate with repository maintainers before publicly disclosing a sensitive finding.
