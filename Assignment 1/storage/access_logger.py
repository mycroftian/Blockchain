from datetime import datetime
from utils.file_utils import get_file_path


def log_access(user_id, patient_id, operation, success=True, details=""):
    try:
        log_file = get_file_path("access.log")
        timestamp = datetime.now().isoformat()
        status = "SUCCESS" if success else "FAILED"

        log_line = f"{timestamp} | {user_id} | {operation} | {patient_id} | {status} | {details}\n"

        with open(log_file, 'a') as f:
            f.write(log_line)
        return True
    except:
        return False


def get_access_logs(user_id=None, patient_id=None, limit=50):
    try:
        log_file = get_file_path("access.log")
        with open(log_file, 'r') as f:
            lines = f.readlines()

        parsed_logs = []
        for line in lines:
            parts = line.strip().split(' | ')
            if len(parts) >= 5:
                log_entry = {
                    'timestamp': parts[0],
                    'user_id': parts[1],
                    'operation': parts[2],
                    'patient_id': parts[3],
                    'success': parts[4] == 'SUCCESS',
                    'details': parts[5] if len(parts) > 5 else ""
                }
                parsed_logs.append(log_entry)

        # Filter logs
        filtered_logs = parsed_logs
        if user_id:
            filtered_logs = [
                log for log in filtered_logs if log['user_id'] == user_id]
        if patient_id:
            filtered_logs = [
                log for log in filtered_logs if log['patient_id'] == patient_id]

        # Sort by timestamp descending and limit
        filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)
        return filtered_logs[:limit]
    except:
        return []
