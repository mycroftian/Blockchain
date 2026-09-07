from datetime import datetime
from crypto.hashing import create_hash
from crypto.digital_signature import verify_signature
from utils.file_utils import load_json_file, save_json_file, get_file_path
from storage.access_logger import log_access
from storage.file_storage import load_users, save_users

# doctors can stake 10+ tokens to become blockchain validators
def stake_tokens(doctor_id, amount, signature):
    MINIMUM_STAKE = 10
    if amount < MINIMUM_STAKE:
        return False, f"Minimum stake required: {MINIMUM_STAKE} tokens"

    try:
        stake_data = {'doctor_id': doctor_id, 'amount': amount, 'action': 'stake'}
        trusted_public_key = get_doctor_public_key(doctor_id)
        if not trusted_public_key:
            log_access(doctor_id, None, "stake_tokens", success=False, details="Doctor's public key not found in users.json")
            return False, "Doctor's public key not found in users.json"
        if not verify_signature(trusted_public_key, signature, stake_data):
            log_access(doctor_id, None, "stake_tokens", success=False, details="Invalid digital signature - unauthorized staking attempt")
            return False, "Invalid digital signature - unauthorized staking attempt"

        stakes = load_stakes()
        tokens = load_users()

        if doctor_id not in tokens or tokens[doctor_id]['tokens'] < amount:
            log_access(doctor_id, None, "stake_tokens", success=False, details="Insufficient tokens to stake")
            return False, "Insufficient tokens to stake"
        
        tokens[doctor_id]['tokens'] -= amount
        if doctor_id in stakes:
            stakes[doctor_id]['amount'] += amount
        else:
            timestamp = datetime.now().isoformat()
            stakes[doctor_id] = {
                'amount': amount,
                'staked_at': timestamp,
                'transaction_hash': create_hash({'doctor_id': doctor_id, 'amount': amount, 'timestamp': timestamp})
            }

        save_stakes(stakes)
        save_users(tokens)
        
        log_access(doctor_id, None, "stake_tokens", success=True, details=f"Staked {amount} tokens for {doctor_id}")
        return True, f"Staked {amount} tokens for {doctor_id}"

    except Exception as e:
        log_access(doctor_id, None, "stake_tokens", success=False, details=f"Error staking tokens: {str(e)}")
        return False, f"Error staking tokens: {str(e)}"


# not implemented in the blockchain yet - generally unstaking is not allowed
def unstake_tokens(doctor_id, amount, signature):
    try:
        unstake_data = {'doctor_id': doctor_id,
                        'amount': amount, 'action': 'unstake'}
        trusted_public_key = get_doctor_public_key(doctor_id)
        if not trusted_public_key:
            log_access(doctor_id, None, "unstake_tokens", success=False, details="Doctor's public key not found in users.json")
            return False, "Doctor's public key not found in users.json"
        if not verify_signature(trusted_public_key, signature, unstake_data):
            log_access(doctor_id, None, "unstake_tokens", success=False, details="Invalid digital signature - unauthorized unstaking attempt")
            return False, "Invalid digital signature - unauthorized unstaking attempt"

        stakes = load_stakes()
        tokens = load_users()

        if doctor_id not in stakes:
            log_access(doctor_id, None, "unstake_tokens", success=False, details="Doctor has no staked tokens")
            return False, "Doctor has no staked tokens"
        if stakes[doctor_id]['amount'] < amount:
            log_access(doctor_id, None, "unstake_tokens", success=False, details="Insufficient staked tokens")
            return False, "Insufficient staked tokens"

        stakes[doctor_id]['amount'] -= amount
        if stakes[doctor_id]['amount'] == 0:
            del stakes[doctor_id]

        tokens[doctor_id]['tokens'] += amount
        save_users(tokens)

        save_stakes(stakes)
        log_access(doctor_id, None, "unstake_tokens", success=True, details=f"Unstaked {amount} tokens for {doctor_id}")
        return True, f"Unstaked {amount} tokens for {doctor_id}"

    except Exception as e:
        log_access(doctor_id, None, "unstake_tokens", success=False, details=f"Error unstaking tokens: {str(e)}")
        return False, f"Error unstaking tokens: {str(e)}"


# not implemented yet - admin can slash stake of malicious validators
def slash_stake(doctor_id, penalty, admin_signature, admin_public_key=None):
    try:
        slash_data = {'doctor_id': doctor_id,
                      'penalty': penalty, 'action': 'slash', 'admin': True}
        trusted_admin_key = None
        if admin_public_key:
            trusted_admin_key = get_doctor_public_key(admin_public_key)
        if not trusted_admin_key:
            log_access(admin_public_key, doctor_id, "slash_stake", success=False, 
                      details="Admin's public key not found in users.json")
            return False, "Admin's public key not found in users.json"
        if not verify_signature(trusted_admin_key, admin_signature, slash_data):
            log_access(admin_public_key, doctor_id, "slash_stake", success=False, 
                      details="Invalid admin signature - unauthorized slashing attempt")
            return False, "Invalid admin signature - unauthorized slashing attempt"

        stakes = load_stakes()
        if doctor_id not in stakes:
            log_access(admin_public_key, doctor_id, "slash_stake", success=False, 
                      details="Doctor has no staked tokens")
            return False, "Doctor has no staked tokens"

        stakes[doctor_id]['amount'] = max(
            0, stakes[doctor_id]['amount'] - penalty)
        if stakes[doctor_id]['amount'] == 0:
            del stakes[doctor_id]

        save_stakes(stakes)
        log_access(admin_public_key, doctor_id, "slash_stake", success=True, 
                  details=f"Slashed {penalty} tokens from {doctor_id}")
        return True, f"Slashed {penalty} tokens from {doctor_id}"

    except Exception as e:
        log_access(admin_public_key, doctor_id, "slash_stake", success=False, 
                  details=f"Error slashing stake: {str(e)}")
        return False, f"Error slashing stake: {str(e)}"


# verify stake integrity by checking the hash - not part of normal operations
def verify_stake_integrity(doctor_id):
    stakes = load_stakes()
    if doctor_id not in stakes:
        return False, "Doctor not found in stakes"

    stake_record = stakes[doctor_id]
    if 'transaction_hash' not in stake_record:
        return True, "No hash to verify (legacy record)"

    expected_data = {
        'doctor_id': doctor_id,
        'amount': stake_record['amount'],
        'timestamp': stake_record['staked_at']
    }
    expected_hash = create_hash(expected_data)

    if expected_hash == stake_record['transaction_hash']:
        return True, "Stake integrity verified"
    else:
        return False, "Stake integrity check failed - possible tampering"


def load_stakes():
    stakes_file = get_file_path("stakes.json")
    return load_json_file(stakes_file, {})


def save_stakes(stakes):
    stakes_file = get_file_path("stakes.json")
    return save_json_file(stakes_file, stakes)


def get_stake_amount(doctor_id):
    stakes = load_stakes()
    return stakes.get(doctor_id, {}).get('amount', 0)


def get_doctor_public_key(doctor_id):
    users_file = get_file_path("users.json")
    users = load_json_file(users_file, {})
    user = users.get(doctor_id)
    if user and 'public_key' in user:
        from cryptography.hazmat.primitives import serialization
        return serialization.load_pem_public_key(user['public_key'].encode())
    return None
