import hashlib
import json

# Create a SHA-256 hash of the transaction data
def create_hash(transaction_data):
    transaction_string = json.dumps(transaction_data, sort_keys=True).encode()
    return hashlib.sha256(transaction_string).hexdigest()