import subprocess
from pathlib import Path
def git(args,cwd=None,timeout=120):
 p=subprocess.run(['git',*args],cwd=cwd,text=True,capture_output=True,timeout=timeout)
 if p.returncode:raise RuntimeError(p.stderr.strip() or p.stdout.strip())
 return p.stdout.strip()
class Worktrees:
 def __init__(self,root):self.root=root;root.mkdir(parents=True,exist_ok=True)
 def create(self,project,tid):
  repo=Path(project['repo']).expanduser().resolve()
  if not repo.is_dir() or not (repo/'.git').exists():raise RuntimeError('Not a git checkout: '+str(repo))
  b='sidekick/'+tid;w=(self.root/tid).resolve();git(['fetch','--all'],repo,180);git(['worktree','add','-b',b,str(w),project.get('default_branch','main')],repo);return str(w),b
