from config import TOKEN, BOT_USERNAME
from telegram import Update
from telegram.ext import ContextTypes, ChatMemberHandler, ApplicationBuilder


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    member = result.new_chat_member
    chat_id = result.chat.id
    name = member.user.first_name
    group = result.chat.title

    if member.status == 'member':
        count = await context.bot.get_chat_member_count(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Welcome {name} to {group}! You're member #{count}.\nEnjoy your stay! Say HI 👋"
        )

    elif member.status == 'left':
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{name} left {group}. We hope they enjoyed their stay :)"
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    print(f"{BOT_USERNAME} is running..")
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    print(f"{BOT_USERNAME} is polling..")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
