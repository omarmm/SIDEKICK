import json
from pathlib import Path
class ProjectRegistry:
 def __init__(self,path):
  if not path.exists(): raise RuntimeError('Copy projects.example.json to projects.json')
  self.projects={p['id']:p for p in json.loads(path.read_text()).get('projects',[])}
 def get(self,pid):return self.projects.get(pid)
 def all(self):return list(self.projects.values())
