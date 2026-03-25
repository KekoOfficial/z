import asyncio
from telegram import Bot
from core.state import chat_activo
from core.users import get_users

TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"
bot = Bot(token=TOKEN)

async def send(uid, msg):
    await bot.send_message(chat_id=uid, text=msg)

def seleccionar_usuario():
    users = get_users()

    print("\n👥 Usuarios disponibles:")
    for uid, name in users.items():
        print(f"{uid} → {name}")

    uid = input("\n🎯 Escribe el ID del usuario: ")

    if uid in users:
        chat_activo["user_id"] = int(uid)
        chat_activo["username"] = users[uid]
        print(f"\n💬 Chat activo con: {users[uid]}")
    else:
        print("❌ Usuario no encontrado")
        seleccionar_usuario()

async def chat():
    while True:
        msg = input("\n>> ")

        if msg == "/exit":
            print("👋 Saliendo...")
            break

        if not chat_activo["user_id"]:
            print("⚠️ No hay usuario seleccionado")
            continue

        await send(chat_activo["user_id"], msg)

async def main():
    print("💀 KHASAM MP CHAT")

    seleccionar_usuario()
    await chat()

if __name__ == "__main__":
    asyncio.run(main())