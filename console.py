import asyncio
from telegram import Bot
from core.state import chat_activo
from core.users import get_users

TOKEN = "8367475601:AAFt-z2bWkFY4W4ReGGVxKSkKtyWr4DkAUY"
bot = Bot(token=TOKEN)

# 🚀 enviar mensaje
async def send(uid, msg):
    try:
        await bot.send_message(chat_id=uid, text=msg)
        print(f"✅ Enviado → {msg}")
    except Exception as e:
        print(f"❌ Error: {e}")

# 👥 mostrar usuarios
def mostrar_usuarios():
    users = get_users()

    print("\n👥 LISTA DE USUARIOS:")
    for uid, name in users.items():
        print(f"{uid} → {name}")

    if not users:
        print("⚠️ No hay usuarios aún")

# 🎯 seleccionar usuario
def seleccionar(uid):
    users = get_users()

    if uid in users:
        chat_activo["user_id"] = int(uid)
        chat_activo["username"] = users[uid]
        print(f"\n💬 Chat activo con: {users[uid]}")
    else:
        print("❌ Usuario no encontrado")

# 🧠 panel principal
async def main():
    print("""
💀 KHASAM MP CONSOLE

Comandos:
users → ver usuarios
select <id> → elegir usuario
exit → salir

Modo rápido:
<ID> mensaje

Modo chat:
(escribe directo después de seleccionar)
""")

    while True:
        cmd = input("\n>> ")

        if not cmd:
            continue

        # 🚪 salir
        if cmd == "exit":
            print("👋 Cerrando consola...")
            break

        # 👥 ver usuarios
        elif cmd == "users":
            mostrar_usuarios()

        # 🎯 seleccionar usuario
        elif cmd.startswith("select"):
            partes = cmd.split()

            if len(partes) < 2:
                print("⚠️ Usa: select <id>")
                continue

            seleccionar(partes[1])

        else:
            partes = cmd.split()

            # 🔥 modo rápido → ID mensaje
            if partes[0].isdigit():
                uid = partes[0]
                mensaje = " ".join(partes[1:])

                if not mensaje:
                    print("⚠️ Escribe un mensaje")
                    continue

                await send(int(uid), mensaje)

            # 💬 modo chat → usuario ya seleccionado
            elif chat_activo["user_id"]:
                await send(chat_activo["user_id"], cmd)

            else:
                print("⚠️ Usa 'select <id>' o escribe: <id> mensaje")

# ▶️ ejecutar
if __name__ == "__main__":
    asyncio.run(main())