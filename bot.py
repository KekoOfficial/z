from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from core.users import save_user
from core.logs import log
from core.state import chat_activo

TOKEN = "TU_TOKEN"

async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    uid = user.id
    name = user.username or user.first_name

    save_user(uid, name)
    log(name, update.message.text)

    # actualizar chat activo
    chat_activo["user_id"] = uid
    chat_activo["username"] = name

    await update.message.reply_text("📩 Recibido")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, recibir))

    print("💀 BOT MP ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()