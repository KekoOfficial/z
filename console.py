import asyncio
from telegram import Bot
from core.state import chat_activo
from core.users import get_users

TOKEN = "TU_TOKEN"
bot = Bot(token=TOKEN)

async def send(uid, msg):
    await bot.send_message(chat_id=uid, text=msg)

def menu():
    print("""
💀 KHASAM MP PANEL

Comandos:
1 → users
2 → select <id>
3 → msg <texto>
4 → exit
""")

async def main():
    while True:
        menu()
        cmd = input(">> ")

        if cmd == "users":
            users = get_users()
            for uid, name in users.items():
                print(f"{uid} → {name}")

        elif cmd.startswith("select"):
            _, uid = cmd.split()
            users = get_users()

            if uid in users:
                chat_activo["user_id"] = int(uid)
                chat_activo["username"] = users[uid]
                print(f"🎯 Seleccionado: {users[uid]}")
            else:
                print("❌ No existe")

        elif cmd.startswith("msg"):
            if not chat_activo["user_id"]:
                print("⚠️ Selecciona usuario primero")
                continue

            mensaje = cmd.replace("msg ", "")
            await send(chat_activo["user_id"], mensaje)

        elif cmd == "exit":
            break

        else:
            print("❌ Comando inválido")

if __name__ == "__main__":
    asyncio.run(main())