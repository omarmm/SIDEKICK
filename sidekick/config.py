from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

BOT_TOKEN = _required("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(_required("TELEGRAM_OWNER_ID"))
HOME = Path(os.getenv("SIDECICK_HOME", "./data")).resolve()
PROJECTS_FILE = Path(os.getenv("PROJECTS_FILE", "./projects.json")).resolve()
MAX_CONCURRENT = max(1, int(os.getenv("MAX_CONCURRENT_TASKS", "1")))
TIMEOUT = max(60, int(os.getenv("TASK_TIMEOUT_SECONDS", "3600")))
OPENCODE_BIN = os.getenv("OPENCODE_BIN", "opencode")
WORKTREES = HOME / "worktrees"
DB = HOME / "sidekick.sqlite3"
