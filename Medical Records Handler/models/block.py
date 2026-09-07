from crypto.hashing import create_hash
from crypto.merkle_tree import build_merkle_tree


class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # List of transaction dicts
        self.timestamp = timestamp
        self.nonce = nonce

        self.merkle_root = self.compute_merkle_root()
        self.block_header_hash = self.compute_hash()  # hash of the block header

    # Computes the hash of the block header
    def compute_hash(self):
        block_header = {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }
        block_header_hash = create_hash(block_header)
        return block_header_hash

    # Computes the Merkle root of the transactions
    def compute_merkle_root(self):
        if not self.transactions:
            return None
        return build_merkle_tree(self.transactions)
