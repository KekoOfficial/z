import json, os
from datetime import datetime

FILE = "data/logs.json"

def log(user, msg):
    os.makedirs("data", exist_ok=True)

    data = []
    if os.path.exists(FILE):
        data = json.load(open(FILE))

    entry = {
        "user": user,
        "msg": msg,
        "time": datetime.now().strftime("%H:%M:%S")
    }

    data.append(entry)
    json.dump(data, open(FILE, "w"), indent=4)

    print(f"\n[{entry['time']}] 💬 {user}: {msg}")