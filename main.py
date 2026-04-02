import os

try:
    from config import TOKEN, BOT_USERNAME
except ImportError:
    TOKEN = os.environ.get("TOKEN")
    BOT_USERNAME = os.environ.get("BOT_USERNAME")

from telegram import Update
from telegram.ext import ContextTypes, ChatMemberHandler, ApplicationBuilder, CommandHandler
import sqlite3

async def setWelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    member = await context.bot.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("You're not an admin!")
        return

    new_message = " ".join(context.args)
    if not new_message:
        await update.message.reply_text("Usage: /setwelcome <message>")
        return
        
    os.makedirs(os.path.expanduser('~/data'), exist_ok=True)
    con = sqlite3.connect(os.path.expanduser('~/data/setWelcome.db'))
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS welcome(chat_id INTEGER PRIMARY KEY, message TEXT)")
    cur.execute("INSERT OR REPLACE INTO welcome(chat_id, message) VALUES (?,?)", (chat_id, new_message))
    con.commit()
    con.close()

    await update.message.reply_text("Welcome message updated!")

async def clearWelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    member = await context.bot.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("You're not an admin!")
        return
    
    con = sqlite3.connect(os.path.expanduser('~/data/setWelcome.db'))
    cur = con.cursor()
    cur.execute("DELETE FROM welcome WHERE chat_id = ?", (chat_id,))
    con.commit()
    con.close()
    
    await update.message.reply_text("Welcome message cleared! Using default now.")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    member = result.new_chat_member
    chat_id = result.chat.id
    name = member.user.first_name
    group = result.chat.title
    count = await context.bot.get_chat_member_count(chat_id)

    if member.status == 'member':
        con = sqlite3.connect(os.path.expanduser('~/data/setWelcome.db'))
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS welcome(chat_id INTEGER PRIMARY KEY, message TEXT)")
        cur.execute("SELECT message FROM welcome WHERE chat_id = ?", (chat_id,))

        row = cur.fetchone()
        con.close()

        if row:
            welcome_text = row[0]

        else:
            welcome_text = f"Welcome {name} to {group}! You're member #{count}.\nEnjoy your stay! Say HI 👋"

        welcome_text = welcome_text.format(name=name, group=group, count=count)


        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_text)

    elif member.status == 'left':
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{name} left {group}. We hope they enjoyed their stay :)"
        )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Greeter Bot Commands:\n\n"
        "/setwelcome <message> - Set custom welcome message\n\n"
        "You can use these placeholders in your message:\n"
        "{name} - Member's first name\n"
        "{group} - Group name\n"
        "{count} - Current member count\n\n"
        "Example:\n"
        "/setwelcome Welcome {name} to {group}! You're member #{count} 🎉\n\n"
        "/clearwelcome - Reset to default welcome message"
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    print(f"{BOT_USERNAME} is running..")

    app.add_handler(CommandHandler("setwelcome", setWelcome))
    app.add_handler(CommandHandler("clearwelcome", clearWelcome))
    app.add_handler(CommandHandler("help", help_cmd))

    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    print(f"{BOT_USERNAME} is polling..")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
