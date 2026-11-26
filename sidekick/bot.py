import logging
from telegram.ext import Application,CommandHandler
from . import config
from .projects import ProjectRegistry
from .store import TaskStore
from .engine import Engine
logging.basicConfig(level=logging.INFO);registry=ProjectRegistry(config.PROJECTS_FILE);store=TaskStore(config.DB);app=Application.builder().token(config.BOT_TOKEN).build()
async def report(chat,msg):await app.bot.send_message(chat_id=chat,text=msg[:4000])
engine=Engine(store,registry,config,report)
def auth(u):return u.effective_user and u.effective_user.id==config.OWNER_ID
async def guard(u):
 if not auth(u):
  if u.message:await u.message.reply_text('Unauthorized');return False
 return True
async def start(u,c):
 if await guard(u):await u.message.reply_text('/projects\n/run PROJECT task\n/tasks\n/status ID')
async def projects(u,c):
 if await guard(u):await u.message.reply_text('\n'.join(x['id'] for x in registry.all()) or 'No projects')
async def run(u,c):
 if not await guard(u):return
 if len(c.args)<2:await u.message.reply_text('Usage: /run PROJECT task');return
 pid,t=c.args[0],' '.join(c.args[1:])
 if not registry.get(pid):await u.message.reply_text('Unknown project');return
 tid=engine.submit(pid,t,u.effective_chat.id);await u.message.reply_text('Queued '+tid)
async def tasks(u,c):
 if await guard(u):await u.message.reply_text('\n'.join(x['id']+' '+x['state'] for x in store.recent()) or 'Empty')
async def status(u,c):
 if not await guard(u):return
 if not c.args:await u.message.reply_text('Usage /status ID');return
 r=store.get(c.args[0]);await u.message.reply_text('Not found' if not r else r['state']+'\n'+(r['result'] or '')[-3000:])
for cmd,fn in [('start',start),('projects',projects),('run',run),('tasks',tasks),('status',status)]:app.add_handler(CommandHandler(cmd,fn))
def main():config.HOME.mkdir(parents=True,exist_ok=True);config.WORKTREES.mkdir(parents=True,exist_ok=True);app.run_polling()
if __name__=='__main__':main()
