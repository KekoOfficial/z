import json, os

FILE = "data/users.json"
os.makedirs("data", exist_ok=True)

def get_users():
    if not os.path.exists(FILE):
        return {}
    return json.load(open(FILE))

def save_user(user_id, username):
    users = get_users()
    users[str(user_id)] = username
    json.dump(users, open(FILE, "w"), indent=4)