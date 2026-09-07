from datetime import datetime
from consensus.staking import load_stakes
from crypto.digital_signature import verify_signature
from storage.access_logger import log_access

# check if doctor is eligible to be a validator based on their stake
def is_eligible_validator(doctor_id):
    try:
        MIN_STAKE_REQUIRED = 10
        stakes = load_stakes()
        if doctor_id not in stakes:
            log_access(doctor_id, None, "is_eligible_validator", success=False, details="Doctor has no staked tokens")
            return False, "Doctor has no staked tokens"

        doctor_stake = stakes[doctor_id]['amount']
        if doctor_stake < MIN_STAKE_REQUIRED:
            log_access(doctor_id, None, "is_eligible_validator", success=False, details=f"Insufficient stake. Required: {MIN_STAKE_REQUIRED}, Current: {doctor_stake}")
            return False, f"Insufficient stake. Required: {MIN_STAKE_REQUIRED}, Current: {doctor_stake}"

        log_access(doctor_id, None, "is_eligible_validator", success=True, details=f"Doctor {doctor_id} is eligible with stake: {doctor_stake}")
        return True, f"Doctor {doctor_id} is eligible with stake: {doctor_stake}"

    except Exception as e:
        log_access(doctor_id, None, "is_eligible_validator", success=False, details=f"Error checking eligibility: {str(e)}")
        return False, f"Error checking eligibility: {str(e)}"

# get list of all active validators
def get_active_validators():
    try:
        stakes = load_stakes()
        MIN_STAKE_REQUIRED = 10
        active_validators = []

        for doctor_id, stake_info in stakes.items():
            if stake_info['amount'] >= MIN_STAKE_REQUIRED:
                active_validators.append({
                    'doctor_id': doctor_id,
                    'stake': stake_info['amount'],
                    'staked_at': stake_info['staked_at']
                })

        active_validators.sort(key=lambda x: x['stake'], reverse=True) # sort by stake - largest to smallest
        return active_validators

    except Exception as e:
        print(f"Error getting active validators: {str(e)}")
        return []

# verify validator's authorization using digital signature
def verify_validator_authorization(doctor_id, signature, public_key, operation):
    try:
        auth_data = {
            'doctor_id': doctor_id,
            'operation': operation,
            'timestamp': datetime.now().isoformat(),
            'role': 'validator'
        }

        if not verify_signature(public_key, signature, auth_data):
            log_access(doctor_id, None, "verify_validator_authorization", success=False, details="Invalid digital signature for validator operation")
            return False, "Invalid digital signature for validator operation"
        eligible, message = is_eligible_validator(doctor_id)
        if not eligible:
            log_access(doctor_id, None, "verify_validator_authorization", success=False, details=f"Doctor not eligible for validator operations: {message}")
            return False, f"Doctor not eligible for validator operations: {message}"

        log_access(doctor_id, None, "verify_validator_authorization", success=True, details="Validator authorization verified")
        return True, "Validator authorization verified"

    except Exception as e:
        log_access(doctor_id, None, "verify_validator_authorization", success=False, details=f"Error verifying validator authorization: {str(e)}")
        return False, f"Error verifying validator authorization: {str(e)}"
