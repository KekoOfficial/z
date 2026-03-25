import json, os
from datetime import datetime

FILE = "data/logs.json"

def log(user, msg):
    os.makedirs("data", exist_ok=True)

    try:
        data = []
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                data = json.load(f)

        entry = {
            "user": user,
            "msg": msg,
            "time": datetime.now().strftime("%H:%M:%S")
        }

        data.append(entry)

        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("❌ Error guardando log:", e)