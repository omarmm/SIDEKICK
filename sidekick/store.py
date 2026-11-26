import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class TaskStore:
    def __init__(self, db: Path):
        db.parent.mkdir(parents=True, exist_ok=True)
        self.db = db
        with self.conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY, project TEXT NOT NULL, prompt TEXT NOT NULL,
                state TEXT NOT NULL, branch TEXT, worktree TEXT, created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL, result TEXT, chat_id INTEGER NOT NULL
            )""")

    def conn(self):
        c = sqlite3.connect(self.db, timeout=30)
        c.row_factory = sqlite3.Row
        return c

    def create(self, task_id, project, prompt, chat_id):
        now = datetime.now(timezone.utc).isoformat()
        with self.conn() as c:
            c.execute("INSERT INTO tasks(id,project,prompt,state,created_at,updated_at,chat_id) VALUES(?,?,?,?,?,?,?)",
                      (task_id, project, prompt, "queued", now, now, chat_id))

    def update(self, task_id, state, **fields):
        now = datetime.now(timezone.utc).isoformat()
        allowed = {"branch", "worktree", "result"}
        values = {k:v for k,v in fields.items() if k in allowed}
        values["state"] = state
        values["updated_at"] = now
        sql = ",".join(f"{k}=?" for k in values)
        with self.conn() as c:
            c.execute(f"UPDATE tasks SET {sql} WHERE id=?", (*values.values(), task_id))

    def get(self, task_id):
        with self.conn() as c:
            row = c.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        return dict(row) if row else None

    def recent(self, limit=10):
        with self.conn() as c:
            rows = c.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
