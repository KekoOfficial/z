import json
import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# --- Config ---
TOKEN = "TU_TOKEN_AQUI"
DATA_FILE = "data/historial.json"

# --- Inicializa historial ---
if not os.path.exists("data"):
    os.makedirs("data")

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        historial = json.load(f)
else:
    historial = {}

# --- Guardar historial ---
def guardar_historial():
    with open(DATA_FILE, "w") as f:
        json.dump(historial, f, indent=4)

# --- Manejar mensajes recibidos ---
async def mensaje_recibido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    mensaje = update.message.text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if user_id not in historial:
        historial[user_id] = []

    historial[user_id].append({
        "timestamp": timestamp,
        "from": update.message.from_user.username or str(user_id),
        "message": mensaje
    })

    guardar_historial()
    print(f"\n📥 Mensaje de {user_id}: {mensaje}\n>> ", end="", flush=True)

# --- Consola para enviar mensajes ---
async def consola(app):
    seleccionado = None

    while True:
        comando = input(">> ").strip()

        if comando.lower() == "users":
            print("👥 Usuarios disponibles:")
            for i, uid in enumerate(historial.keys(), 1):
                print(f"{i} → {uid}")
        elif comando.startswith("select"):
            try:
                idx = int(comando.split()[1]) - 1
                seleccionado = list(historial.keys())[idx]
                print(f"✅ Chat seleccionado: {seleccionado}")
            except:
                print("❌ ID inválido")
        elif comando.startswith("hist"):
            try:
                uid = comando.split()[1]
                print(f"📜 Historial de {uid}:")
                for m in historial.get(uid, []):
                    print(f"{m['timestamp']} | {m['from']} → {m['message']}")
            except:
                print("❌ Comando inválido")
        elif comando.lower() in ["exit", ".e"]:
            print("Saliendo de consola...")
            break
        elif seleccionado:
            mensaje = comando
            await app.bot.send_message(chat_id=int(seleccionado), text=mensaje)

            # Guardar en historial
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            historial[seleccionado].append({
                "timestamp": timestamp,
                "from": "BOT",
                "message": mensaje
            })
            guardar_historial()
            print(f"✅ Mensaje enviado a {seleccionado}: {mensaje}")
        else:
            print("❌ Selecciona un chat primero con: select <número>")

# --- Ejecutar bot ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mensaje_recibido))

    # Correr consola y bot al mismo tiempo
    await asyncio.gather(
        app.start(),
        consola(app)
    )

    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot detenido.")