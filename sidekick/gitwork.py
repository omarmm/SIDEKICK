import subprocess
from pathlib import Path

def run_git(args, cwd=None, timeout=120):
    p = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip() or f"git exited {p.returncode}")
    return p.stdout.strip()

class WorktreeManager:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)

    def prepare(self, project, task_id):
        repo = Path(project["repo"]).expanduser().resolve()
        if not repo.is_dir() or not (repo / ".git").exists():
            raise RuntimeError(f"Repository path invalid or not a Git checkout: {repo}")
        branch = f"sidekick/{task_id}"
        wt = (self.root / task_id).resolve()
        run_git(["fetch", "--all"], cwd=repo, timeout=180)
        base = project.get("default_branch", "main")
        run_git(["worktree", "add", "-b", branch, str(wt), base], cwd=repo)
        return str(wt), branch

    def cleanup(self, repo, worktree):
        run_git(["worktree", "remove", "--force", worktree], cwd=repo)
