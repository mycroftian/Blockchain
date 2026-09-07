from utils.file_utils import load_json_file, get_file_path
from storage.access_logger import log_access


def authorize_access(user_id, patient_id, operation):
    try:
        user_information = get_file_path("users.json")
        users = load_json_file(user_information, {})
        if user_id not in users:
            log_access(user_id, patient_id, f"authorize_access_{operation}", success=False, details="User not found in system")
            return False

        user_role = users[user_id].get('role', '').lower()
        if operation == "read":
            authorized = user_role in ["patient", "doctor", "admin"] and (user_id == patient_id or user_role in ["doctor", "admin"])
        elif operation == "write":
            authorized = user_role in ["doctor", "admin"]
        else:
            authorized = False
        
        if not authorized:
            log_access(user_id, patient_id, f"authorize_access_{operation}", success=False, details=f"Insufficient permissions for {operation} operation")
        else:
            log_access(user_id, patient_id, f"authorize_access_{operation}", success=True, details=f"Access granted for {operation} operation")

        return authorized
    except Exception as e:
        log_access(user_id, patient_id, f"authorize_access_{operation}", success=False, details=f"Authorization error: {str(e)}")
        return False
