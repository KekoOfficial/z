import os
import json
import asyncio
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔑 Token del bot
TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"

# Carpeta y archivo de historial
DATA_DIR = "data"
HISTORIAL_FILE = os.path.join(DATA_DIR, "historial.json")
os.makedirs(DATA_DIR, exist_ok=True)

# Chat activo
chat_activo = {"user_id": None, "username": None}

# Guardar historial
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

# Leer historial por usuario
def leer_historial(uid=None, last_n=10):
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, "r") as f:
        historial = json.load(f)
    if uid:
        historial = [m for m in historial if m["uid"] == uid]
    return historial[-last_n:]

# Mostrar los últimos mensajes al iniciar
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

    # Guardar en historial
    guardar_historial(name, uid, contenido, tipo)

    # Mostrar en consola
    print(f"\n💀 [{name}] ({uid}) → {contenido} ({tipo})")

    # Actualizar chat activo
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

# Bucle de consola dentro del bot
async def consola(bot: Bot):
    print("\n💀 PANEL DE ADMIN - Escribe tu mensaje")
    print("Comandos disponibles:")
    print("users -> mostrar últimos usuarios")
    print("hist <uid> -> ver últimos 10 mensajes de un usuario")
    print("exit -> salir del panel")
    print("Si hay chat activo, solo escribe y se enviará\n")

    while True:
        cmd = input(">> ")

        if not cmd:
            continue

        # salir
        if cmd.lower() == "exit":
            print("👋 Cerrando panel...")
            break

        # mostrar usuarios recientes
        elif cmd.lower() == "users":
            historial = leer_historial(last_n=50)
            usuarios = {}
            for m in historial:
                usuarios[m["uid"]] = m["user"]
            print("\n👥 Usuarios recientes:")
            for uid, name in usuarios.items():
                print(f"{uid} → {name}")

        # mostrar historial de un usuario
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

        # enviar mensaje a chat activo
        elif chat_activo["user_id"]:
            await enviar_msg(bot, chat_activo["user_id"], cmd)

        else:
            # enviar mensaje con id directo
            partes = cmd.split()
            if partes[0].isdigit():
                uid = int(partes[0])
                mensaje = " ".join(partes[1:])
                if not mensaje:
                    print("⚠️ Escribe un mensaje después del ID")
                    continue
                await enviar_msg(bot, uid, mensaje)
            else:
                print("⚠️ No hay chat activo y no se detectó ID. Usa users o hist <uid>")

# Iniciar bot y consola al mismo tiempo
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, recibir))

    print("💀 BOT MP ACTIVO CON HISTORIAL Y MEMORIA AL REINICIAR")
    mostrar_ultimo_historial(n=20)

    loop = asyncio.get_event_loop()
    bot = Bot(token=TOKEN)
    # Ejecutar bot y consola al mismo tiempo
    loop.create_task(app.run_polling(drop_pending_updates=True))
    loop.run_until_complete(consola(bot))

if __name__ == "__main__":
    main()