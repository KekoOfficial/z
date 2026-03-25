import os
import json
import asyncio
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔑 Token
TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"

# Carpeta y archivo historial
DATA_DIR = "data"
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial.json")
os.makedirs(DATA_DIR, exist_ok=True)

# Últimos usuarios para seleccionar rápido
chat_activo = {"user_id": None, "username": None}

# Guardar mensaje
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

# Leer historial
def leer_historial(uid=None, last_n=10):
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, "r") as f:
        historial = json.load(f)
    if uid:
        historial = [m for m in historial if m["uid"] == uid]
    return historial[-last_n:]

# Mostrar últimos mensajes al iniciar
def mostrar_ultimo_historial(n=20):
    historial = leer_historial(last_n=n)
    if historial:
        print("📜 Últimos mensajes antes del reinicio:")
        for m in historial:
            print(f"{m['time']} | {m['user']} ({m['uid']}) → {m['msg']} ({m['tipo']})")
    else:
        print("⚠️ No hay mensajes guardados aún")

# Detectar tipo de mensaje
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

# Recibir mensajes
async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.message.from_user
    uid = user.id
    name = user.username or user.first_name
    contenido, tipo = detectar_contenido(update.message)

    guardar_historial(name, uid, contenido, tipo)

    # Mostrar en consola en tiempo real
    print(f"\n💀 [{name}] ({uid}) → {contenido} ({tipo})")

    # Actualizar chat activo automáticamente
    chat_activo["user_id"] = uid
    chat_activo["username"] = name

# Enviar mensaje
async def enviar_msg(bot, uid, mensaje):
    try:
        await bot.send_message(chat_id=uid, text=mensaje)
        print(f"✅ Mensaje enviado a {uid}: {mensaje}")
        guardar_historial("ADMIN", uid, mensaje, "texto")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

# Consola asíncrona para enviar mensajes en tiempo real
async def consola(bot: Bot):
    print("\n💀 PANEL ADMIN - Chat en tiempo real")
    print("Comandos:")
    print("users -> últimos usuarios")
    print("hist <uid> -> últimos mensajes")
    print("<uid> <mensaje> -> enviar mensaje directo")
    print("exit -> salir\n")

    loop = asyncio.get_event_loop()
    while True:
        # input no bloqueante usando run_in_executor
        cmd = await loop.run_in_executor(None, input, ">> ")

        if not cmd:
            continue

        if cmd.lower() == "exit":
            print("👋 Cerrando panel...")
            break

        elif cmd.lower() == "users":
            historial = leer_historial(last_n=50)
            usuarios = {}
            for m in historial:
                usuarios[m["uid"]] = m["user"]
            print("\n👥 Usuarios recientes:")
            for uid, name in usuarios.items():
                print(f"{uid} → {name}")

        elif cmd.lower().startswith("hist"):
            partes = cmd.split()
            if len(partes) < 2:
                print("⚠️ Usa: hist <uid>")
                continue
            uid = int(partes[1])
            msgs = leer_historial(uid=uid, last_n=10)
            print(f"\n📜 Últimos mensajes de {uid}:")
            for m in msgs:
                print(f"{m['time']} | {m['user']} → {m['msg']} ({m['tipo']})")

        elif cmd[0].isdigit():
            partes = cmd.split()
            uid = int(partes[0])
            mensaje = " ".join(partes[1:])
            if not mensaje:
                print("⚠️ Escribe un mensaje después del ID")
                continue
            await enviar_msg(bot, uid, mensaje)

        elif chat_activo["user_id"]:
            # enviar al chat activo automáticamente
            await enviar_msg(bot, chat_activo["user_id"], cmd)

        else:
            print("⚠️ No hay chat activo ni ID especificado. Usa users o hist <uid>")

# Iniciar bot y consola juntos
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, recibir))

    print("💀 BOT MP ACTIVO - Chat en consola con historial")
    mostrar_ultimo_historial(n=20)

    loop = asyncio.get_event_loop()
    bot = Bot(token=TOKEN)
    # Ejecutar bot y consola al mismo tiempo
    loop.create_task(app.run_polling(drop_pending_updates=True))
    loop.run_until_complete(consola(bot))

if __name__ == "__main__":
    main()