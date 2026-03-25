import os
import json
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"

# Carpeta para historial
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial.json")

# Guardar mensaje en historial
def guardar_historial(uid, username, mensaje, tipo="texto"):
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r") as f:
            try:
                historial = json.load(f)
            except:
                historial = []
    historial.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uid": uid,
        "user": username,
        "msg": mensaje,
        "tipo": tipo
    })
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f, indent=2)

# Manejar mensajes recibidos
async def mensaje_recibido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    username = update.effective_user.username or update.effective_user.full_name
    texto = update.message.text if update.message else ""
    guardar_historial(uid, username, texto, tipo="texto")
    print(f"📩 {username} ({uid}) → {texto}")

# Manejar errores
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"❌ ERROR: {context.error}")

# Función principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler de mensajes
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_recibido))
    # Handler de errores
    app.add_error_handler(error_handler)

    print("💀 BOT ACTIVADO")
    print("Esperando mensajes...")

    # Run polling sin conflictos
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()