import random
from consensus.staking import load_stakes, get_stake_amount, save_stakes
from consensus.validator import get_active_validators, is_eligible_validator
from storage.access_logger import log_access
from storage.file_storage import load_users, save_users

# Proof of Stake (PoS) consensus mechanism implementation
# Weighteed random selection of validator based on their stake
def select_validator():
    active_validators = get_active_validators() 

    if not active_validators:
        log_access(None, None, "select_validator", success=False, details="No active validators available for selection")
        raise Exception("No active validators available for selection")

    doctor_ids = [v['doctor_id'] for v in active_validators]    
    stakes = [v['stake'] for v in active_validators]

    chosen = random.choices(doctor_ids, weights=stakes, k=1)[0]     
    log_access(chosen, None, "select_validator", success=True, details=f"Validator {chosen} selected for consensus")
    
    return chosen


# After successfully validating a block, reward the validator with 10 tokens
def reward_validator(doctor_id, reward_amount=10):
    stakes = load_stakes()   
    tokens = load_users()
    if doctor_id not in stakes:
        log_access(doctor_id, None, "reward_validator", success=False, details=f"Validator {doctor_id} not found in stake records")
        return False, f"Validator {doctor_id} not found in stake records"

    tokens[doctor_id]['tokens'] += reward_amount             
    save_stakes(stakes)
    save_users(tokens)

    log_access(doctor_id, None, "reward_validator", success=True, details=f"Validator {doctor_id} rewarded with {reward_amount} tokens")

    return True, f"Validator {doctor_id} rewarded with {reward_amount} tokens"


# Penalize a validator for malicious behavior - not implemented in blockchain yet
def penalize_validator(doctor_id, penalty_amount=10):
    stakes = load_stakes()

    if doctor_id not in stakes:
        log_access(doctor_id, None, "penalize_validator", success=False, details=f"Validator {doctor_id} not found in stake records")
        return False, f"Validator {doctor_id} not found in stake records"

    stakes[doctor_id]['amount'] = max(0, stakes[doctor_id]['amount'] - penalty_amount)

    if stakes[doctor_id]['amount'] == 0:
        del stakes[doctor_id]  # remove the validator if stake is wiped out fully

    save_stakes(stakes)
    log_access(doctor_id, None, "penalize_validator", success=True, details=f"Validator {doctor_id} penalized by {penalty_amount} tokens")

    return True, f"Validator {doctor_id} penalized by {penalty_amount} tokens"

# Validate a block proposal - not implemented in blockchain yet
def validate_block_proposal(doctor_id):
    eligible, message = is_eligible_validator(doctor_id)
    return eligible, message


