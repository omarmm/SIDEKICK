# Sidekick

**Your personal AI software engineering assistant.**

You assign the task. Sidekick gets to work.

Sidekick is a mobile-first personal agent that accepts software-development tasks through Telegram, understands repository context and specifications, executes work in isolated Git worktrees using OpenCode, verifies changes, and reports back.

## MVP goal

Send a task from your phone and have Sidekick safely carry it through:

1. Identify the configured repository.
2. Inspect project instructions and relevant specifications.
3. Create an isolated Git worktree and task branch.
4. Run OpenCode to execute the task.
5. Run configured verification commands.
6. Report results and optionally commit/push/create a pull request.

Merge and deployment remain approval-gated.

## Initial architecture

- **Telegram:** mobile interface (long polling for local MVP)
- **Orchestrator:** Python
- **Execution engine:** OpenCode CLI
- **Isolation:** Git worktrees
- **Repositories:** GitHub
- **Initial persistence:** SQLite
- **Initial runtime:** developer laptop
- **Queue/concurrency:** in-process queue and bounded concurrency initially

## Scope boundaries for v0.1

- One user (owner allowlist).
- Explicitly configured repositories.
- Task lifecycle tracking.
- Isolated worktrees.
- OpenCode execution.
- Basic verification.
- Telegram progress and completion reports.
- No automatic merge or deployment.
- No unrestricted host access; execution boundaries must be documented and enforced as far as the MVP environment allows.

## Roadmap

See [specs](specs/) and [project-state.md](project-state.md).

## Status

Early foundation. Specifications and security boundaries are being established before implementation.
