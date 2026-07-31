# Visual Identity

## Repository image pack

The reusable repository assets live in `docs/assets/brand/`:

- `logo-transparent.png` is the full-resolution transparent mark.
- `logo-1024.png`, `logo-512.png`, and `logo-256.png` are padded size variants.
- `logo-mask.svg` is the editable single-color variant.
- `cover-1280x640.png` is the normalized cover.
- `social-card.png` combines the cover with the mark.
- `manifest.json` records source hashes, dimensions, processing settings, and validation.

The mark combines a checked payload, a bounded queue path, and a verification seal. The cover shows the implemented flow from payloads through local validation and controlled host execution to durable reports. These assets describe the harness boundary; they do not represent host-side execution as locally guaranteed.

## Brand palette

| Role | Color |
| --- | --- |
| Deep navy | `#10233A` |
| Primary teal | `#0C6B69` |
| Signal green | `#82B84B` |
| Muted amber | `#E2A82B` |
| Warm ivory | `#F1E8D1` |

## Implemented presentation conventions

- CLI results are formatted as indented, key-sorted JSON.
- Saved reports and validation bundles are formatted as indented, key-sorted JSON with a trailing newline.
- Smoke payloads use the `NexusSmoke` naming prefix for generated scene objects and assets.
- The material smoke payload uses `Universal Render Pipeline/Lit` and sets `_Smoothness` to `0.25`. This is test input, not a shared material, palette, or styling standard.
- Particle and terrain smoke payload values exercise functionality only; they do not define visual direction.

## Boundaries

- This repository does not own the Unity package source or its Editor control surface.
- Do not treat generated smoke scenes, materials, terrain, or particle configurations as brand assets or approved art direction.
- No checked-in logo, palette, typography system, icon set, UI layout, screenshot baseline, or visual asset library was found.

## Usage and accessibility

- Use the transparent logo only over backgrounds that maintain clear edge contrast.
- Use meaningful alt text describing payload validation, controlled queue execution, and report evidence.
- Do not crop, stretch, rotate, recolor the multicolor PNG, or add effects to the mark.
- Do not use smoke payload content as approved visual art direction; those values exist to exercise behavior.

## Regeneration

Regenerate through the Repo Image Studio workflow documented in `docs/assets/brand/README.md`. Validate the manifest, dimensions, alpha corners, mask coverage, and full-frame composition, then visually inspect the transparent logo, cover, and social card before replacement.
