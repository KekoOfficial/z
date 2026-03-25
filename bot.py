import json
from datetime import datetime
from threading import Thread
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

HISTORIAL_FILE = "data/historial.json"
TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"

# Cargar historial
def cargar_historial():
    try:
        with open(HISTORIAL_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def guardar_historial(historial):
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f, indent=4)

historial = cargar_historial()
bot = Bot(TOKEN)

# Recibir mensajes
async def mensaje_recibido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat_id)
    text = update.message.text
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if user_id not in historial:
        historial[user_id] = []
    historial[user_id].append({"ts": ts, "from": "user", "text": text})
    guardar_historial(historial)

    print(f"\n📩 {ts} | {user_id} → {text}\n>> ", end="")

# Consola para enviar mensajes
def consola():
    global historial
    chat_seleccionado = None

    while True:
        cmd = input(">> ").strip()

        if cmd == "users":
            print("👥 Usuarios:")
            for i, uid in enumerate(historial.keys(), 1):
                print(f"{i} → {uid}")

        elif cmd.startswith("select"):
            parts = cmd.split()
            if len(parts) == 2 and parts[1].isdigit():
                idx = int(parts[1]) - 1
                usuarios = list(historial.keys())
                if 0 <= idx < len(usuarios):
                    chat_seleccionado = usuarios[idx]
                    print(f"✅ Chat seleccionado: {chat_seleccionado}")
                else:
                    print("❌ Índice inválido")
            else:
                print("❌ Comando inválido")

        elif cmd.startswith("hist"):
            parts = cmd.split()
            if len(parts) == 2:
                uid = parts[1]
                if uid in historial:
                    print(f"📜 Últimos mensajes de {uid}:")
                    for msg in historial[uid]:
                        print(f"{msg['ts']} | {msg['from']} → {msg['text']}")
                else:
                    print("❌ Usuario no encontrado")
            else:
                print("❌ Comando inválido")

        elif chat_seleccionado:
            text = cmd
            bot.send_message(chat_id=chat_seleccionado, text=text)
            historial[chat_seleccionado].append({"ts": "Ahora", "from": "me", "text": text})
            guardar_historial(historial)
            print(f"✅ Mensaje enviado a {chat_seleccionado}: {text}")

        else:
            print("❌ Selecciona un chat primero con: select <número>")

# Iniciar bot y consola en paralelo
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mensaje_recibido))

print("💀 BOT ACTIVADO")

# Hilo de consola
Thread(target=consola, daemon=True).start()

# Ejecutar bot
app.run_polling(drop_pending_updates=True)