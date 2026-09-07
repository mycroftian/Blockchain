from utils.file_utils import load_json_file, save_json_file, get_file_path
from crypto.encryption import generate_symmetric_key

# Manages shared symmetric keys between doctors and patients
def get_or_create_shared_key(doctor_id, patient_id):
    key_file = get_file_path("shared_keys.json")
    composite_key = f"{doctor_id}-{patient_id}"
    shared_keys = load_json_file(key_file, {})

    if composite_key in shared_keys:
        return shared_keys[composite_key].encode('latin-1')
    else:
        new_key_as_bytes = generate_symmetric_key()
        new_key_as_str = new_key_as_bytes.decode('latin-1')
        shared_keys[composite_key] = new_key_as_str

        save_json_file(key_file, shared_keys, indent=4)
        return new_key_as_bytes

# Optional - Delete a shared key if needed
def delete_shared_key(doctor_id, patient_id):
    key_file = get_file_path("shared_keys.json")
    composite_key = f"{doctor_id}-{patient_id}"
    shared_keys = load_json_file(key_file, {})

    if composite_key in shared_keys:
        del shared_keys[composite_key]
        save_json_file(key_file, shared_keys, indent=4)
        return True
    return False

# List all shared keys (for admin use) - not typically exposed
def list_shared_keys():
    key_file = get_file_path("shared_keys.json")
    return load_json_file(key_file, {})
