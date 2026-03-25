import os
import json
import asyncio
from telegram import Bot

# 🔑 Token del bot
TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"

# Carpeta compartida con bot.py
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial.json")

# Función para leer historial
def leer_historial(uid=None, last_n=10):
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, "r") as f:
        historial = json.load(f)
    if uid:
        historial = [m for m in historial if m["uid"] == uid]
    return historial[-last_n:]

# Función para enviar mensaje a usuario
async def enviar_msg(bot, uid, mensaje):
    try:
        await bot.send_message(chat_id=uid, text=mensaje)
        print(f"✅ Mensaje enviado a {uid}: {mensaje}")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

# Consola interactiva
async def consola():
    bot = Bot(token=TOKEN)
    print("💀 PANEL ADMIN ACTIVO")
    print("Comandos:")
    print("users -> últimos usuarios")
    print("hist <uid> -> últimos mensajes")
    print("<uid> <mensaje> -> enviar mensaje directo")
    print("exit -> salir\n")

    loop = asyncio.get_event_loop()
    while True:
        cmd = await loop.run_in_executor(None, input, ">> ")
        if not cmd:
            continue

        # Salir
        if cmd.lower() == "exit":
            break

        # Mostrar usuarios recientes
        elif cmd.lower() == "users":
            historial = leer_historial(last_n=50)
            usuarios = {}
            for m in historial:
                usuarios[m["uid"]] = m["user"]
            print("👥 Usuarios recientes:")
            for uid, name in usuarios.items():
                print(f"{uid} → {name}")

        # Mostrar historial de un usuario
        elif cmd.lower().startswith("hist"):
            partes = cmd.split()
            if len(partes) < 2:
                print("⚠️ Usa: hist <uid>")
                continue
            uid = int(partes[1])
            msgs = leer_historial(uid=uid, last_n=10)
            print(f"📜 Últimos mensajes de {uid}:")
            for m in msgs:
                print(f"{m['time']} | {m['user']} → {m['msg']} ({m['tipo']})")

        # Enviar mensaje directo a ID
        elif cmd[0].isdigit():
            partes = cmd.split()
            uid = int(partes[0])
            mensaje = " ".join(partes[1:])
            if not mensaje:
                print("⚠️ Escribe un mensaje después del ID")
                continue
            await enviar_msg(bot, uid, mensaje)

        else:
            print("⚠️ Comando no reconocido")

if __name__ == "__main__":
    asyncio.run(consola())