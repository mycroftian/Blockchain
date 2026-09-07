import time
from models.block import Block
from storage.file_storage import load_users
from crypto.digital_signature import verify_signature
from cryptography.hazmat.primitives import serialization

# Get a validator's public key from their user ID
def get_validator_public_key(validator_id):
    users = load_users()
    validator_info = users.get(validator_id)
    if not validator_info or 'public_key' not in validator_info:
        return None
    try:
        public_key_pem = validator_info['public_key'].encode()
        return serialization.load_pem_public_key(public_key_pem)
    except Exception:
        return None


class Blockchain:
    def __init__(self):
        self.chain = []
        # creates the empty chain with its list of pending transactions
        self.pending_transactions = []

        genesis_block = Block(  # genesis block (the first block) is created
            index=0,
            previous_hash="0",
            transactions=[],
            timestamp=time.time(),
            nonce=0
        )
        genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]  # gives the most recent block in the blockchain

    def is_chain_valid(self):  # validates the chain
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current['previous_hash'] != previous['block_header_hash']:
                print(f"Chain broken: Block {current['index']} previous_hash does not match Block {previous['index']} hash.")
                return False

            temp_block = Block(
                index=current['index'],
                previous_hash=current['previous_hash'],
                transactions=current['transactions'],
                timestamp=current['timestamp'],
                nonce=current['nonce']
            )
            if temp_block.block_header_hash != current['block_header_hash']:
                print(f"Chain broken: Block {current['index']} hash is invalid.")
                return False
            
            validator_id = current.get('validator_id')
            block_signature_hex = current.get('block_signature')

            if not validator_id or not block_signature_hex:
                print(f"Chain broken: Block {current['index']} is missing validator signature.")
                return False

            public_key = get_validator_public_key(validator_id)
            if not public_key:
                print(f"Chain broken: Could not find public key for validator {validator_id}.")
                return False

            data_to_verify = {
                'index': current['index'],
                'previous_hash': current['previous_hash'],
                'transactions': current['transactions'],
                'timestamp': current['timestamp'],
                'nonce': current['nonce']
            }
            
            signature_bytes = bytes.fromhex(block_signature_hex)
            
            if not verify_signature(public_key, signature_bytes, data_to_verify):
                print(f"Chain broken: Invalid signature on Block {current['index']} from validator {validator_id}.")
                return False

        return True
