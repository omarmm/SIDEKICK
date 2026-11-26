import asyncio,uuid,subprocess
from .gitwork import Worktrees,git
from .runner import Runner
class Engine:
 def __init__(self,store,registry,cfg,report):
  self.store,self.registry,self.cfg,self.report=store,registry,cfg,report;self.sem=asyncio.Semaphore(cfg.MAX_CONCURRENT);self.wt=Worktrees(cfg.WORKTREES);self.runner=Runner(cfg.OPENCODE_BIN,cfg.TIMEOUT);self.active={}
 def submit(self,pid,prompt,chat):
  tid=uuid.uuid4().hex[:8];self.store.create(tid,pid,prompt,chat);asyncio.create_task(self.run_task(tid));return tid
 async def run_task(self,tid):
  async with self.sem:
   r=self.store.get(tid);p=self.registry.get(r['project'])
   if not p:self.store.update(tid,'failed',result='Unknown project');await self.report(r['chat_id'],'Unknown project');return
   try:
    self.store.update(tid,'preparing');w,b=await asyncio.to_thread(self.wt.create,p,tid);self.active[tid]=w;self.store.update(tid,'running',branch=b,worktree=w)
    prompt='Read repo instructions and relevant specs. Do not push, merge or deploy. Implement this task and test it.\nTASK:\n'+r['prompt'];code,out=await asyncio.to_thread(self.runner.run,prompt,w);self.store.update(tid,'verifying');checks=[]
    for cmd in p.get('verification',[]):
     x=await asyncio.to_thread(subprocess.run,cmd,cwd=w,shell=True,text=True,capture_output=True,timeout=300);checks.append(cmd+' exit='+str(x.returncode)+'\n'+x.stdout[-2000:]);code=code or x.returncode
    summary='Exit: '+str(code)+'\n'+out[-8000:]+('\nChecks:\n'+'\n'.join(checks) if checks else '')
    if code==0 and p.get('auto_commit',False):
     await asyncio.to_thread(git,['add','-A'],w)
     if await asyncio.to_thread(git,['status','--porcelain'],w):
      await asyncio.to_thread(git,['commit','-m','Sidekick '+tid],w)
      if p.get('auto_push',False):await asyncio.to_thread(git,['push','-u','origin',b],w);summary+='\nPushed '+b
    s='completed' if code==0 else 'failed';self.store.update(tid,s,result=summary);await self.report(r['chat_id'],tid+' '+s+'\n'+summary[:3500])
   except Exception as e:self.store.update(tid,'failed',result=str(e));await self.report(r['chat_id'],tid+' FAILED: '+str(e))
   finally:self.active.pop(tid,None)
