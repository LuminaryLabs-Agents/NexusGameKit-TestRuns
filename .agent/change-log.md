# Change Log

This log records verified repository-level changes and clearly separates current implementation from planned work.

## 2026-07-31 - Documentation and visual package

- Added maintainer onboarding, architecture, CLI, payload-contract, operations, validation, contribution, and visual-identity guidance.
- Added an operational `.agent/` workspace and durable repository profile.
- Added a validated repository image pack under `docs/assets/brand/`.
- Preserved the harness implementation, workflows, tests, payloads, manifests, and repository settings.

## 0.1.0 - Initial harness baseline

### Implemented

- Added a Python external validation harness for Nexus Game Kit queue payloads.
- Added local payload validation with canonical action recognition, legacy-action warnings, and structural error reporting.
- Added CLI commands for payload validation, directory validation, action-payload generation, RPC health checks, queue checks, and queue submission with optional waiting.
- Added JSON run and validation-bundle report writing.
- Added smoke payload examples covering scene, hierarchy and transform, material, particle, terrain, and scene-save flows.
- Added automated Python unit tests and a workflow that validates smoke payloads and uploads its report artifact.
- Added a manually dispatched live-host smoke workflow that validates and submits a selected payload, then uploads reports.

### Planned

- Add small Unity runner projects for the Unity 2020 and Unity 6 package tracks when those tracks are ready for editor validation.

### Unknown / not established

- No release date or publication status is documented for 0.1.0.
- No recorded live-host execution result or Unity editor-validation result is present in this checkout.
- The registered `build-actions` CLI path is not operational in the current baseline because its parser rejects the intended action tokens; only the underlying builder helpers have direct test coverage.
