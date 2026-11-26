# Architecture — Initial

## Components

### Telegram adapter
Receives owner commands, performs authorization, and sends task status and reports. Initially uses long polling.

### Orchestrator
Validates requests, creates task records, coordinates preparation, execution, verification, cancellation, and reporting.

### Project registry
Stores explicitly configured project identifiers, repository locations, execution settings, and verification commands.

### Worktree manager
Creates and tracks per-task worktrees and branches, and performs safe cleanup.

### OpenCode runner
Invokes the OpenCode CLI as a subprocess, captures output, applies timeouts, and exposes cancellation.

### Verification runner
Runs configured verification steps and records exit codes and output summaries.

### Persistence
SQLite stores task metadata, state, timestamps, workspace references, and execution results.

## Initial flow

Telegram -> authorization -> request validation -> task record -> worktree -> context discovery -> OpenCode -> verification -> report

Optional Git publishing stages will be added only after execution and verification are stable.

## Isolation caveat

Git worktrees isolate files and branches, but they do not provide operating-system security isolation. Processes launched by the coding agent may still have access to the host environment according to the permissions of the user running Sidekick. Stronger isolation (containers, restricted users, or other sandboxing) must be considered before exposing Sidekick beyond the trusted owner or running untrusted repositories/tasks.
