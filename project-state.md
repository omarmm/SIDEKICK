# Sidekick Project State

## Current milestone

**M0 — Foundation and MVP specification**

## Status

Repository initialized. Foundation documents created. Implementation has not started.

## Next task

**T001 — Foundation Specification and Project Skeleton**

Produce and approve the detailed implementation specification, package structure, configuration model, task lifecycle, and baseline tests before implementing the Telegram-to-agent workflow.

## MVP milestone sequence

- M0: Foundation, scope, architecture, security boundaries
- M1: Telegram interface and owner authentication
- M2: Project registry and task lifecycle
- M3: Worktree manager and isolated execution
- M4: OpenCode runner and output capture
- M5: Verification pipeline
- M6: Git commit/push and PR workflow
- M7: Persistence, recovery, concurrency and operational hardening

## Decisions already made

- Local laptop-first prototype.
- Telegram long polling; no webhook required for the initial local prototype.
- Python orchestrator.
- OpenCode CLI as the initial coding engine.
- Git worktrees for task isolation.
- GitHub for source control and pull requests.
- SQLite initially; avoid introducing Redis or distributed infrastructure in the MVP.
- Bounded concurrency.
- Merge and deployment require explicit user approval.

## Change discipline

Update this file when milestones or significant decisions change. Keep implementation tasks and verification evidence traceable to specifications.
