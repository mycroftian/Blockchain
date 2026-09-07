import json
import os


def load_json_file(file_path, default_value=None):
    try:
        if not os.path.exists(file_path):
            return default_value if default_value is not None else {}
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return default_value if default_value is not None else {}


def save_json_file(file_path, data, indent=2):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception:
        return False


def append_to_json_list(file_path, new_item, max_items=None):
    try:
        items = load_json_file(file_path, [])
        if not isinstance(items, list):
            items = []
        items.append(new_item)
        if max_items and len(items) > max_items:
            items = items[-max_items:]
        return save_json_file(file_path, items)
    except Exception:
        return False


def ensure_data_directory(base_path="data"):
    os.makedirs(base_path, exist_ok=True)
    return base_path


def get_file_path(filename, directory="data"):
    return os.path.join(directory, filename)


def get_user_id_by_name(name):
    users_file = get_file_path("users.json")
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
        for user_id, user in users.items():
            if user.get('name') == name:
                return user_id
    return None
