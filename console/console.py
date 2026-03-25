import os
import json
import asyncio
from telegram import Bot

TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial.json")

# Leer historial
def leer_historial(uid=None, last_n=10):
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, "r") as f:
        historial = json.load(f)
    if uid:
        historial = [m for m in historial if m["uid"] == uid]
    return historial[-last_n:]

# Enviar mensaje a usuario
async def enviar_msg(bot, uid, mensaje):
    try:
        await bot.send_message(chat_id=uid, text=mensaje)
        print(f"✅ Mensaje enviado a {uid}: {mensaje}")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

# Consola interactiva estilo chat
async def consola():
    bot = Bot(token=TOKEN)
    print("💀 PANEL ADMIN ACTIVO")
    print("Comandos:")
    print("users -> últimos usuarios")
    print("hist <uid> -> últimos mensajes")
    print("exit -> salir del panel\n")

    loop = asyncio.get_event_loop()
    chat_uid = None  # Usuario actualmente seleccionado
    usuarios_lista = []

    while True:
        if chat_uid:
            prompt = f"[Chat con {chat_uid}] >> "
        else:
            prompt = ">> "
        cmd = await loop.run_in_executor(None, input, prompt)
        if not cmd:
            continue

        # Salir del panel
        if cmd.lower() == "exit":
            break

        # Mostrar usuarios recientes
        elif cmd.lower() == "users":
            historial = leer_historial(last_n=50)
            usuarios = {}
            for m in historial:
                usuarios[m["uid"]] = m["user"]
            usuarios_lista = list(usuarios.items())
            print("👥 Usuarios recientes:")
            for idx, (uid, name) in enumerate(usuarios_lista, start=1):
                print(f"{idx} {uid} → {name}")

        # Ver historial de un usuario
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

        # Seleccionar usuario por número de lista
        elif cmd.isdigit() and usuarios_lista:
            idx = int(cmd) - 1
            if 0 <= idx < len(usuarios_lista):
                chat_uid = usuarios_lista[idx][0]
                print(f"💬 Chat seleccionado con {usuarios_lista[idx][1]} ({chat_uid})")
            else:
                print("⚠️ Número inválido")

        # Salir del chat actual
        elif cmd == ".e":
            chat_uid = None
            print("🔹 Saliste del chat actual")

        # Enviar mensaje al usuario seleccionado
        elif chat_uid:
            await enviar_msg(bot, chat_uid, cmd)

        else:
            print("⚠️ Comando no reconocido. Usa 'users' para ver lista de usuarios o 'exit' para salir")

if __name__ == "__main__":
    asyncio.run(consola())