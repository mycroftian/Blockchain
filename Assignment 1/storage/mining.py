from utils.file_utils import get_file_path
from storage.access_logger import log_access
from storage.file_storage import load_pending_transactions, save_pending_transactions, load_blockchain, save_blockchain
from consensus.validator import is_eligible_validator
from consensus.pos import select_validator,reward_validator
from models.block import Block
from crypto.digital_signature import sign_data
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def mine_pending_transactions(validator_id, private_key):
    # Only the selected validator can mine
    try:
        selected_validator = select_validator()
    except Exception as e:
        log_access(validator_id, None, "mine_pending_transactions",
                   success=False, details=f"Validator selection error: {e}")
        return False, f"Validator selection error: {e}"

    if validator_id != selected_validator:
        log_access(validator_id, None, "mine_pending_transactions",
                   success=False, details="Not the selected validator")
        return False, "You are not the selected validator for this round. Only the selected validator can mine a block."

    eligible, msg = is_eligible_validator(validator_id)
    if not eligible:
        log_access(validator_id, None, "mine_pending_transactions",
                   success=False, details=msg)
        return False, f"Not eligible to validate: {msg}"

    pending = load_pending_transactions()
    if not pending or len(pending) == 0:
        log_access(validator_id, None, "mine_pending_transactions",
                   success=False, details="No pending transactions")
        return False, "No pending transactions to mine."

    to_mine = pending[:3]
    if len(to_mine) < 3:
        log_access(validator_id, None, "mine_pending_transactions",
                   success=False, details="Fewer than 3 pending transactions")
        return False, "At least 3 pending transactions required to mine a block."

    # Create new block
    blockchain = load_blockchain()
    last_block = blockchain[-1] if blockchain else None
    prev_header_hash = last_block.get(
        'block_header_hash', '0') if last_block else '0'
    block_index = len(blockchain)
    timestamp = time.time()
    nonce = 0

    block_obj = Block(
        index=block_index,
        previous_hash=prev_header_hash,
        transactions=to_mine,
        timestamp=timestamp,
        nonce=nonce
    )
    block_header_hash = block_obj.compute_hash()

    block_data = {
        'index': block_index,
        'previous_hash': prev_header_hash,
        'transactions': to_mine,
        'timestamp': timestamp,
        'nonce': nonce
    }
    block_signature = sign_data(private_key, block_data)

    block_dict = {
        'index': block_index,
        'previous_hash': prev_header_hash,
        'transactions': to_mine,
        'timestamp': timestamp,
        'nonce': nonce,
        'merkle_root': block_obj.merkle_root,
        'block_header_hash': block_header_hash,
        'validator_id': validator_id,
        'block_signature': block_signature.hex()  # store as hex string
    }

    # Add block to blockchain and update pending transactions
    blockchain.append(block_dict)
    save_blockchain(blockchain)

    pending = pending[3:]
    save_pending_transactions(pending)

    reward_validator(validator_id)

    log_access(validator_id, None, "mine_pending_transactions", success=True,
               details=f"Block {block_index} mined with 3 transactions.")
    return True, f"Block {block_index} successfully mined with 3 transactions."
