import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
def req(k):
 v=os.getenv(k,'').strip()
 if not v: raise RuntimeError('Missing '+k)
 return v
BOT_TOKEN=req('TELEGRAM_BOT_TOKEN'); OWNER_ID=int(req('TELEGRAM_OWNER_ID'))
HOME=Path(os.getenv('SIDECICK_HOME','./data')).resolve(); PROJECTS_FILE=Path(os.getenv('PROJECTS_FILE','./projects.json')).resolve()
MAX_CONCURRENT=max(1,int(os.getenv('MAX_CONCURRENT_TASKS','1'))); TIMEOUT=int(os.getenv('TASK_TIMEOUT_SECONDS','3600')); OPENCODE_BIN=os.getenv('OPENCODE_BIN','opencode')
WORKTREES=HOME/'worktrees'; DB=HOME/'sidekick.sqlite3'
