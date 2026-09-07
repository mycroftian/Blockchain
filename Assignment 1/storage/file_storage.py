from utils.file_utils import load_json_file, save_json_file, get_file_path


def load_blockchain():
    return load_json_file(get_file_path("blockchain.json"), [])


def save_blockchain(blockchain_data):
    return save_json_file(get_file_path("blockchain.json"), blockchain_data)


def load_users():
    return load_json_file(get_file_path("users.json"), {})


def save_users(users_data):
    return save_json_file(get_file_path("users.json"), users_data)


def load_pending_transactions():
    return load_json_file(get_file_path("pending_transactions.json"), [])


def save_pending_transactions(transactions):
    return save_json_file(get_file_path("pending_transactions.json"), transactions)
