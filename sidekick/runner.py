import subprocess,os,signal
class Runner:
 def __init__(self,bin,timeout):self.bin=bin;self.timeout=timeout
 def run(self,prompt,cwd):
  p=subprocess.Popen([self.bin,'run',prompt],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,start_new_session=True)
  try:o,_=p.communicate(timeout=self.timeout)
  except subprocess.TimeoutExpired:
   try:os.killpg(p.pid,signal.SIGTERM)
   except ProcessLookupError:pass
   raise RuntimeError('OpenCode timeout')
  return p.returncode,o
