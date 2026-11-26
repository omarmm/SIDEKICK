# Specification 001 — Foundation and MVP

## 1. Objective

Build a laptop-first, Telegram-controlled personal software engineering assistant that can safely execute coding tasks against configured Git repositories using OpenCode in isolated Git worktrees and report results to its owner.

## 2. Primary user

A single authorized owner using Telegram from a mobile device.

## 3. Core user journey

1. Owner submits a task for a configured project.
2. Sidekick validates the sender and project.
3. Sidekick creates a tracked task.
4. Sidekick prepares a dedicated branch and Git worktree.
5. Sidekick gathers repository instructions and relevant context.
6. Sidekick invokes OpenCode with the task and context.
7. Sidekick runs project verification commands from an approved configuration.
8. Sidekick reports outcome, relevant logs/summary, and changed files.
9. When configured and explicitly allowed, Sidekick may commit, push, and open a PR.
10. Merge and deployment remain outside the automatic MVP workflow.

## 4. MVP requirements

### R1 — Owner authorization
Only configured Telegram user IDs may issue commands or receive project/task information.

### R2 — Project registry
Projects must be explicitly registered with a stable identifier and repository path/URL. Unknown projects must be rejected.

### R3 — Task lifecycle
Each task must have an ID and state. Initial states:
- queued
- preparing
- running
- verifying
- completed
- failed
- cancelled
- awaiting_approval

Invalid transitions must be rejected.

### R4 — Isolation
Each task must execute in its own Git worktree and branch. The orchestrator must not run task edits directly against the primary checkout.

### R5 — Agent execution
The initial execution engine is OpenCode CLI. Invocation must be constructed safely without shell-string interpolation of user task content.

### R6 — Verification
Verification commands must be project-configured and controlled. Results and exit status must be captured.

### R7 — Reporting
Telegram reports must include task ID, project, state, summary, verification result, and branch/PR information when available.

### R8 — Concurrency
Concurrency must be bounded by configuration. The initial implementation may use an in-process queue/semaphore.

### R9 — Cancellation
Owner may request cancellation. The orchestrator must terminate the associated process where feasible and clean up task state safely. Cleanup must not destroy user data.

### R10 — Persistence
Task records must survive orchestrator restarts. SQLite is the initial persistence layer.

### R11 — Git operations
Commit/push/PR operations must be explicit configuration-driven stages. No automatic merge or deployment in MVP.

### R12 — Configuration and secrets
Secrets must not be committed. Configuration errors should fail fast with actionable messages.

## 5. Security baseline

- Telegram owner allowlist.
- Explicit project allowlist.
- Worktree isolation.
- No arbitrary project path supplied by chat messages.
- No shell interpolation of untrusted task text.
- Limit task concurrency and execution duration.
- Redact secrets from reports and logs where practical.
- Treat repository content, issue text, and task inputs as untrusted instructions/data.
- Do not automatically merge or deploy.
- Document limitations of local process/worktree isolation; worktrees alone are not a sandbox.

## 6. Initial commands (candidate interface)

- /start — introduction and help
- /projects — list configured projects
- /run <project> <task> — create and execute a task
- /tasks — list recent tasks
- /status <task_id> — inspect task
- /cancel <task_id> — request cancellation

Command details will be finalized in the implementation specification.

## 7. Non-goals for MVP

- Multi-user tenancy.
- Distributed workers.
- Kubernetes.
- Redis.
- Web dashboard.
- Automatic merge/deployment.
- Autonomous changes across multiple repositories in one task.
- Persistent semantic memory.
- Arbitrary shell commands initiated directly by Telegram.

## 8. Acceptance criteria for the foundation task

- Architecture and boundaries documented.
- Python package structure proposed and justified.
- Configuration schema defined.
- Task lifecycle and transition rules defined.
- Worktree lifecycle defined.
- OpenCode invocation contract defined.
- Security risks and mitigations documented.
- Test strategy defined.
- No implementation begins until these foundation artifacts are reviewed.
