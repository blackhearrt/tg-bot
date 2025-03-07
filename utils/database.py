import json
from pathlib import Path

USER_IDS_FILE = Path("user_ids.json")
ADMIN_IDS = Path("admins.json")


def load_chat_ids():
    if not USER_IDS_FILE.exists():
        return {}
    try:
        with open(USER_IDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

registered_users = load_chat_ids()

def save_chat_ids(user_data):
    with open(USER_IDS_FILE, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

def load_admins():
    if not ADMIN_IDS.exists():
        return set()
    try:
        with open(ADMIN_IDS, "r", encoding="utf-8") as file:
            data = json.load(file)
            return set(data.get("admins", []))
    except json.JSONDecodeError:
        return set()

def save_admins(admins):
    with open(ADMIN_IDS, "w", encoding="utf-8") as file:
        json.dump({"admins": list(admins)}, file, indent=4, ensure_ascii=False)