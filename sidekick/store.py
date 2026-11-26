import sqlite3
from datetime import datetime,timezone
class TaskStore:
 def __init__(self,db):
  db.parent.mkdir(parents=True,exist_ok=True);self.db=db
  with self.conn() as c:c.execute('CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,project TEXT,prompt TEXT,state TEXT,branch TEXT,worktree TEXT,created_at TEXT,updated_at TEXT,result TEXT,chat_id INTEGER)')
 def conn(self):
  c=sqlite3.connect(self.db,timeout=30);c.row_factory=sqlite3.Row;return c
 def create(self,i,p,t,ch):
  n=datetime.now(timezone.utc).isoformat()
  with self.conn() as c:c.execute('INSERT INTO tasks(id,project,prompt,state,created_at,updated_at,chat_id) VALUES(?,?,?,?,?,?,?)',(i,p,t,'queued',n,n,ch))
 def update(self,i,s,**f):
  v={k:x for k,x in f.items() if k in ('branch','worktree','result')};v.update(state=s,updated_at=datetime.now(timezone.utc).isoformat())
  with self.conn() as c:c.execute('UPDATE tasks SET '+','.join(k+'=?' for k in v)+' WHERE id=?',(*v.values(),i))
 def get(self,i):
  with self.conn() as c:r=c.execute('SELECT * FROM tasks WHERE id=?',(i,)).fetchone()
  return dict(r) if r else None
 def recent(self,n=10):
  with self.conn() as c:r=c.execute('SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?',(n,)).fetchall()
  return [dict(x) for x in r]
