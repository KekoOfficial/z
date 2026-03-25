import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"
DATA_DIR = "data"
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial.json")
os.makedirs(DATA_DIR, exist_ok=True)

def guardar_historial(user, uid, contenido, tipo):
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r") as f:
            historial = json.load(f)
    entrada = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "uid": uid,
        "tipo": tipo,
        "msg": contenido
    }
    historial.append(entrada)
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f, indent=4)

def detectar_contenido(msg):
    if msg.text:
        return msg.text, "texto"
    elif msg.photo:
        return "📷 Foto", "foto"
    elif msg.video:
        return "🎬 Video", "video"
    elif msg.audio:
        return "🎵 Audio", "audio"
    elif msg.voice:
        return "🎤 Voz", "voz"
    elif msg.document:
        return "📄 Archivo", "archivo"
    elif msg.sticker:
        return "😂 Sticker", "sticker"
    else:
        return "📦 Otro tipo", "otro"

async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.message.from_user
    uid = user.id
    name = user.username or user.first_name
    contenido, tipo = detectar_contenido(update.message)
    guardar_historial(name, uid, contenido, tipo)
    print(f"[{name}] ({uid}) → {contenido} ({tipo})")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, recibir))
    print("💀 BOT MP ACTIVO")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()