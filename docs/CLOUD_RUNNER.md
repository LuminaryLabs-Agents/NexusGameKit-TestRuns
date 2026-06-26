# Cloud Runner

The cloud runner consumes Nexus Game Kit as a dependency. It should not copy the Unity package source into this repository.

## Responsibilities

- Check out this runner repository.
- Install or reference the target Nexus Game Kit package.
- Run local payload checks.
- Optionally connect to a live Unity host.
- Store JSON reports as artifacts.
- Keep generated prototype publishing behind explicit approval.

## Non-goals

- Owning the Game Kit package source.
- Storing Unity credentials in git.
- Mutating Unity project files without going through the Game Kit queue surface.
