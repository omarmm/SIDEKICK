# Initial Architecture Decisions

## D001 — Laptop-first
Start on the developer laptop to validate the workflow without infrastructure overhead.

## D002 — Telegram long polling
Use Telegram long polling for the local prototype. Webhooks and public endpoints are unnecessary initially.

## D003 — OpenCode CLI
Use OpenCode CLI as the initial coding/execution engine behind an adapter boundary.

## D004 — Git worktrees
Create a separate worktree and branch for each task to prevent tasks from editing the primary checkout or colliding with each other.

## D005 — SQLite initially
Use SQLite for task persistence; avoid external database infrastructure in the MVP.

## D006 — Approval before merge/deploy
Sidekick may prepare and publish changes according to configured policy, but merging and deployment require explicit owner approval.

## D007 — Bounded concurrency
Limit concurrent execution. Start conservatively and make the limit configurable.

## D008 — Worktree is not a sandbox
Worktree isolation is source-control/workspace isolation, not security isolation. Host process permissions must be considered separately.
