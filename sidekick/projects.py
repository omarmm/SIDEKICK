import json
from pathlib import Path

class ProjectRegistry:
    def __init__(self, path: Path):
        self.path = path
        if not path.exists():
            raise RuntimeError(f"Projects config not found: {path}. Copy projects.example.json to projects.json and edit it.")
        data = json.loads(path.read_text())
        self.projects = {p["id"]: p for p in data.get("projects", [])}

    def get(self, project_id):
        return self.projects.get(project_id)

    def all(self):
        return list(self.projects.values())
