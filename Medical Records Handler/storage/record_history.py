from storage.file_storage import load_blockchain, load_users, load_pending_transactions
from storage.access_logger import log_access
from storage.key_manager import get_or_create_shared_key
from crypto.encryption import decrypt_data


def get_patient_record_history(patient_id):
    patient_records = []
    users = load_users()

    # Get confirmed records from blockchain
    blockchain_data = load_blockchain()
    for block in blockchain_data:
        for transaction in block.get('transactions', []):
            if transaction.get('patient_id') == patient_id:
                record = _process_transaction_record(
                    transaction, block, users, status='confirmed'
                )
                if record:
                    patient_records.append(record)

    # Get pending records
    pending_transactions = load_pending_transactions()
    for transaction in pending_transactions:
        if transaction.get('patient_id') == patient_id:
            record = _process_transaction_record(
                transaction, {'block_header_hash': 'pending'}, users, status='pending'
            )
            if record:
                patient_records.append(record)

    # Sort by timestamp
    patient_records.sort(key=lambda x: x['timestamp'])
    return patient_records


def get_doctor_records(doctor_id):
    doctor_records = []
    users = load_users()

    # Get confirmed records from blockchain
    blockchain_data = load_blockchain()
    for block in blockchain_data:
        for transaction in block.get('transactions', []):
            if transaction.get('doctor_id') == doctor_id:
                record = _process_transaction_record(
                    transaction, block, users, status='confirmed'
                )
                if record:
                    doctor_records.append(record)

    # Get pending records
    pending_transactions = load_pending_transactions()
    for transaction in pending_transactions:
        if transaction.get('doctor_id') == doctor_id:
            record = _process_transaction_record(
                transaction, {'block_header_hash': 'pending'}, users, status='pending'
            )
            if record:
                doctor_records.append(record)

    # Sort by timestamp
    doctor_records.sort(key=lambda x: x['timestamp'])
    return doctor_records


def get_records_by_type(record_type):
    type_records = []
    users = load_users()

    # Get confirmed records from blockchain
    blockchain_data = load_blockchain()
    for block in blockchain_data:
        for transaction in block.get('transactions', []):
            if transaction.get('record_type') == record_type:
                record = _process_transaction_record(
                    transaction, block, users, status='confirmed'
                )
                if record:
                    type_records.append(record)

    # Get pending records
    pending_transactions = load_pending_transactions()
    for transaction in pending_transactions:
        if transaction.get('record_type') == record_type:
            record = _process_transaction_record(
                transaction, {'block_header_hash': 'pending'}, users, status='pending'
            )
            if record:
                type_records.append(record)

    # Sort by timestamp
    type_records.sort(key=lambda x: x['timestamp'])
    return type_records


def _process_transaction_record(transaction, block, users, status):
    doctor_id = transaction.get('doctor_id', '')
    patient_id = transaction.get('patient_id', '')

    # Get user names
    doctor_name = transaction.get('doctor_name', users.get(
        doctor_id, {}).get('name', 'Unknown'))
    patient_name = transaction.get('patient_name', users.get(
        patient_id, {}).get('name', 'Unknown'))

    # Log access
    log_access(doctor_id, patient_id, "get_patient_record_history",
               success=True, details=f"{status.title()} record access")

    # Decrypt prescription data
    encrypted_prescription_str = transaction.get('prescription', '')
    decrypted_prescription = "Decryption key not found"

    try:
        shared_key = get_or_create_shared_key(doctor_id, patient_id)
        decrypted_prescription = decrypt_data(
            shared_key, encrypted_prescription_str)
    except Exception as e:
        decrypted_prescription = f"[Decryption error: {e}]"

    # Build record
    record = {
        'block_number': block.get('index', 'pending') if status == 'confirmed' else 'pending',
        'timestamp': transaction.get('timestamp', ''),
        'doctor_id': doctor_id,
        'doctor_name': doctor_name,
        'patient_id': patient_id,
        'patient_name': patient_name,
        'hospital_id': transaction.get('hospital_id', ''),
        'insurance_id': transaction.get('insurance_id', ''),
        'record_id': transaction.get('record_id', ''),
        'record_type': transaction.get('record_type', ''),
        'operation': transaction.get('operation', ''),
        'prescription': decrypted_prescription,
        'amount': transaction.get('amount', ''),
        'block_header_hash': block.get('block_header_hash', ''),
        'status': status
    }

    return record


def search_records(search_criteria):
    all_records = []
    users = load_users()

    # Collect all records
    blockchain_data = load_blockchain()
    for block in blockchain_data:
        for transaction in block.get('transactions', []):
            record = _process_transaction_record(
                transaction, block, users, status='confirmed'
            )
            if record:
                all_records.append(record)

    pending_transactions = load_pending_transactions()
    for transaction in pending_transactions:
        record = _process_transaction_record(
            transaction, {'block_header_hash': 'pending'}, users, status='pending'
        )
        if record:
            all_records.append(record)

    # Filter based on criteria
    filtered_records = []
    for record in all_records:
        if _matches_criteria(record, search_criteria):
            filtered_records.append(record)

    # Sort by timestamp
    filtered_records.sort(key=lambda x: x['timestamp'])
    return filtered_records


def _matches_criteria(record, criteria):
    for key, value in criteria.items():
        if not value:  # Skip empty criteria
            continue

        if key == 'patient_id' and record.get('patient_id') != value:
            return False
        elif key == 'doctor_id' and record.get('doctor_id') != value:
            return False
        elif key == 'record_type' and record.get('record_type') != value:
            return False
        elif key == 'hospital_id' and record.get('hospital_id') != value:
            return False
        elif key == 'date_from' and record.get('timestamp') < value:
            return False
        elif key == 'date_to' and record.get('timestamp') > value:
            return False

    return True
