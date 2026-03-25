from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from core.users import save_user
from core.logs import log
from core.state import chat_activo

TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"

# 🔥 detectar tipo de mensaje
def detectar_contenido(msg):
    if msg.text:
        return msg.text
    elif msg.photo:
        return "📷 Foto"
    elif msg.video:
        return "🎬 Video"
    elif msg.audio:
        return "🎵 Audio"
    elif msg.voice:
        return "🎤 Voz"
    elif msg.document:
        return "📄 Archivo"
    elif msg.sticker:
        return "😂 Sticker"
    else:
        return "📦 Otro"

# 💬 recibir mensajes
async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.message.from_user
    uid = user.id
    name = user.username or user.first_name

    contenido = detectar_contenido(update.message)

    # guardar datos
    save_user(uid, name)
    log(name, contenido)

    # actualizar chat activo
    chat_activo["user_id"] = uid
    chat_activo["username"] = name

    # mostrar en consola PRO
    print(f"\n💀 [{name}] ({uid}) → {contenido}")

    await update.message.reply_text("📩 Recibido")

# 🚀 iniciar bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # 🔥 capturar TODO
    app.add_handler(MessageHandler(filters.ALL, recibir))

    print("💀 BOT MP ACTIVO (Nivel Khasam)")
    app.run_polling()

if __name__ == "__main__":
    main()