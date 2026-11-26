import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from . import config
from .projects import ProjectRegistry
from .store import TaskStore
from .engine import TaskEngine

logging.basicConfig(level=logging.INFO)
registry = ProjectRegistry(config.PROJECTS_FILE)
store = TaskStore(config.DB)

async def send_report(chat_id, message):
    app = application
    await app.bot.send_message(chat_id=chat_id, text=message[:4000])

engine = TaskEngine(store, registry, config, send_report)
application = Application.builder().token(config.BOT_TOKEN).build()

def authorized(update):
    return update.effective_user and update.effective_user.id == config.OWNER_ID

async def guard(update, context):
    if not authorized(update):
        if update.message: await update.message.reply_text("Unauthorized.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, context): return
    await update.message.reply_text(
        "Sidekick MVP 0.1\n\n"
        "/projects — configured projects\n"
        "/run PROJECT task description — run task\n"
        "/tasks — recent tasks\n"
        "/status ID — task details\n"
        "/help — help\n\n"
        "Execution is isolated in Git worktrees. Merge/deploy are not automated."
    )

async def projects_cmd(update, context):
    if not await guard(update, context): return
    items = registry.all()
    await update.message.reply_text("\n".join(f"{p['id']} — {p.get('name',p['id'])}" for p in items) or "No projects configured.")

async def run_cmd(update, context):
    if not await guard(update, context): return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /run PROJECT task description")
        return
    project_id, prompt = context.args[0], " ".join(context.args[1:])
    if not registry.get(project_id):
        await update.message.reply_text("Unknown project. Use /projects.")
        return
    tid = engine.create_task(project_id, prompt, update.effective_chat.id)
    await update.message.reply_text(f"Queued task {tid}\nProject: {project_id}")

async def tasks_cmd(update, context):
    if not await guard(update, context): return
    rows = store.recent()
    await update.message.reply_text("\n".join(f"{r['id']} | {r['project']} | {r['state']}" for r in rows) or "No tasks yet.")

async def status_cmd(update, context):
    if not await guard(update, context): return
    if not context.args:
        await update.message.reply_text("Usage: /status TASK_ID"); return
    r = store.get(context.args[0])
    if not r: await update.message.reply_text("Task not found."); return
    await update.message.reply_text(f"{r['id']} | {r['project']} | {r['state']}\nBranch: {r['branch']}\n\n{(r['result'] or '')[-3500:]}")

async def help_cmd(update, context):
    await start(update, context)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_cmd))
application.add_handler(CommandHandler("projects", projects_cmd))
application.add_handler(CommandHandler("run", run_cmd))
application.add_handler(CommandHandler("tasks", tasks_cmd))
application.add_handler(CommandHandler("status", status_cmd))

def main():
    config.HOME.mkdir(parents=True, exist_ok=True)
    config.WORKTREES.mkdir(parents=True, exist_ok=True)
    application.run_polling()

if __name__ == "__main__":
    main()
