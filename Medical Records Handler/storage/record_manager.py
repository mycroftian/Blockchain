# Import all functions from the new modular structure
from storage.mining import mine_pending_transactions
from storage.key_manager import get_or_create_shared_key
from storage.medical_records import (
    add_medical_record,
    append_medical_record,
    share_medical_record,
    validate_record_data
)
from storage.record_history import (
    get_patient_record_history,
    get_doctor_records,
    get_records_by_type,
    search_records
)

# Re-export all functions for backward compatibility
__all__ = [
    'mine_pending_transactions',
    'get_or_create_shared_key',
    'add_medical_record',
    'append_medical_record',
    'share_medical_record',
    'validate_record_data',
    'get_patient_record_history',
    'get_doctor_records',
    'get_records_by_type',
    'search_records'
]