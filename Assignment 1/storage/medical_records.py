from utils.file_utils import load_json_file, save_json_file, get_file_path
from utils.access_control import authorize_access
from storage.access_logger import log_access
from storage.key_manager import get_or_create_shared_key
from crypto.digital_signature import verify_signature
from crypto.encryption import encrypt_data
from datetime import datetime
import base64


def add_medical_record(doctor_id, patient_id, record_data, signature):
    authorized = authorize_access(doctor_id, patient_id, "write") # Check authorization

    if not authorized:
        log_access(doctor_id, patient_id, "add_medical_record",
                   success=False, details="Authorization failed")
        return False, "Authorization failed"

    # Verify digital signature
    users = load_json_file(get_file_path("users.json"), {})
    doctor = users.get(doctor_id)
    if not doctor or 'public_key' not in doctor:
        log_access(doctor_id, patient_id, "add_medical_record",
                   success=False, details="Doctor public key not found")
        return False, "Doctor public key not found"

    from cryptography.hazmat.primitives import serialization
    public_key = serialization.load_pem_public_key(doctor['public_key'].encode())

    tx_data = {
        'doctor_id': doctor_id,
        'patient_id': patient_id,
        'record_data': record_data
    }

    if not verify_signature(public_key, signature, tx_data):
        log_access(doctor_id, patient_id, "add_medical_record",
                   success=False, details="Invalid digital signature")
        return False, "Invalid digital signature"

    # Encrypt sensitive data
    sensitive_data = record_data.get('prescription', '')
    shared_key = get_or_create_shared_key(doctor_id, patient_id)
    encrypted_prescription = encrypt_data(shared_key, sensitive_data)
    encrypted_prescription_str = base64.b64encode(encrypted_prescription).decode('utf-8')

    # Create transaction
    transaction = {
        'hospital_id': record_data.get('hospital_id', ''),
        'doctor_id': doctor_id,
        'doctor_name': record_data.get('doctor_name', ''),
        'patient_id': patient_id,
        'patient_name': record_data.get('patient_name', ''),
        'insurance_id': record_data.get('insurance_id', ''),
        'record_id': record_data.get('record_id', ''),
        'record_type': record_data.get('record_type', ''),
        'operation': record_data.get('operation', ''),
        'prescription': encrypted_prescription_str,
        'amount': record_data.get('amount', 0.0),
        'timestamp': record_data.get('timestamp') or datetime.now().isoformat()
    }

    # Save to pending transactions
    pending_file = get_file_path("pending_transactions.json")
    try:
        pending_transactions = load_json_file(pending_file, [])
        pending_transactions.append(transaction)
        save_json_file(pending_file, pending_transactions)
        log_access(doctor_id, patient_id, "add_medical_record",
                   success=True, details="Record added successfully")
        return True, "Record added successfully"

    except Exception as e:
        log_access(doctor_id, patient_id, "add_medical_record",
                   success=False, details=f"Error: {str(e)}")
        return False, f"Error: {str(e)}"


def append_medical_record(doctor_id, patient_id, record_data, signature):
    record_data['operation'] = 'update'
    return add_medical_record(doctor_id, patient_id, record_data, signature)


def share_medical_record(doctor_id, patient_id, record_data, signature):
    record_data['operation'] = 'share'
    return add_medical_record(doctor_id, patient_id, record_data, signature)


def validate_record_data(record_data):
    required_fields = ['doctor_id', 'patient_id']

    for field in required_fields:
        if field not in record_data or not record_data[field]:
            return False, f"Missing required field: {field}"

    # Validate record type if provided
    valid_record_types = ['diagnosis',
                          'prescription', 'test_result', 'consultation']
    if 'record_type' in record_data and record_data['record_type'] not in valid_record_types:
        return False, f"Invalid record type. Must be one of: {valid_record_types}"

    # Validate operation if provided
    valid_operations = ['add', 'update', 'share']
    if 'operation' in record_data and record_data['operation'] not in valid_operations:
        return False, f"Invalid operation. Must be one of: {valid_operations}"

    return True, "Record data is valid"
