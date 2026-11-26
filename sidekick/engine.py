import asyncio, uuid, subprocess
from pathlib import Path
from .gitwork import WorktreeManager, run_git
from .runner import OpenCodeRunner

class TaskEngine:
    def __init__(self, store, registry, config, reporter):
        self.store, self.registry, self.config, self.reporter = store, registry, config, reporter
        self.sem = asyncio.Semaphore(config.MAX_CONCURRENT)
        self.worktrees = WorktreeManager(config.WORKTREES)
        self.runner = OpenCodeRunner(config.OPENCODE_BIN, config.TIMEOUT)
        self.active = {}

    def create_task(self, project_id, prompt, chat_id):
        task_id = uuid.uuid4().hex[:8]
        self.store.create(task_id, project_id, prompt, chat_id)
        asyncio.create_task(self.process(task_id))
        return task_id

    async def process(self, task_id):
        async with self.sem:
            row = self.store.get(task_id)
            project = self.registry.get(row["project"])
            if not project:
                self.store.update(task_id, "failed", result="Unknown project")
                await self.reporter(row["chat_id"], f"Task {task_id}: unknown project.")
                return
            wt = None
            try:
                self.store.update(task_id, "preparing")
                wt, branch = await asyncio.to_thread(self.worktrees.prepare, project, task_id)
                self.store.update(task_id, "running", branch=branch, worktree=wt)
                self.active[task_id] = wt
                prompt = (
                    "You are a coding agent operating on this task in an isolated git worktree. "
                    "Follow repository instructions (including AGENTS.md and relevant specs). "
                    "Do not modify unrelated files, do not merge, deploy, or push. "
                    "Make the requested change, run appropriate tests if possible, and summarize.\n\nTASK:\n" + row["prompt"]
                )
                code, output = await asyncio.to_thread(self.runner.execute, prompt, wt)
                self.store.update(task_id, "verifying")
                verification = []
                for command in project.get("verification", []):
                    # Configuration-only command list; task text cannot add commands.
                    p = await asyncio.to_thread(subprocess.run, command, cwd=wt, shell=True,
                        text=True, capture_output=True, timeout=300)
                    verification.append(f"$ {command}\nexit={p.returncode}\n{p.stdout}\n{p.stderr}")
                    if p.returncode: code = code or p.returncode
                summary = f"OpenCode exit code: {code}\n\nOutput (tail):\n{output[-12000:]}"
                if verification: summary += "\n\nConfigured verification:\n" + "\n\n".join(verification)
                if code == 0 and project.get("auto_commit", False):
                    await asyncio.to_thread(run_git, ["add", "-A"], wt)
                    # Prevent empty commit.
                    status = await asyncio.to_thread(run_git, ["status", "--porcelain"], wt)
                    if status:
                        await asyncio.to_thread(run_git, ["commit", "-m", f"sidekick: {task_id}"], wt)
                        if project.get("auto_push", False):
                            await asyncio.to_thread(run_git, ["push", "-u", "origin", branch], wt)
                            summary += f"\n\nPushed branch: {branch}"
                state = "completed" if code == 0 else "failed"
                self.store.update(task_id, state, result=summary)
                await self.reporter(row["chat_id"], f"Task {task_id} — {state}\nProject: {row['project']}\nBranch: {branch}\n\n{summary}")
            except Exception as e:
                self.store.update(task_id, "failed", result=str(e))
                await self.reporter(row["chat_id"], f"Task {task_id} failed: {e}")
            finally:
                self.active.pop(task_id, None)
