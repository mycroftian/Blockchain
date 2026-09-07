from cryptography.fernet import Fernet, InvalidToken
from base64 import b64decode

# Generate a symmetric key for encryption/decryption of medical records
def generate_symmetric_key():
    return Fernet.generate_key()

# Encrypt the data using the symmetric key
def encrypt_data(symmetric_key, trans_data):
    fernet = Fernet(symmetric_key)
    trans_data_bytes = trans_data.encode()
    encrypted_data = fernet.encrypt(trans_data_bytes)
    return encrypted_data

# Decrypt the data using the symmetric key
def decrypt_data(symmetric_key, encrypted_data):
    try:
        encrypted_data_bytes = b64decode(encrypted_data)
        fernet = Fernet(symmetric_key)
        decrypted_data_bytes = fernet.decrypt(encrypted_data_bytes)
        return decrypted_data_bytes.decode()
    except InvalidToken:
        raise ValueError("Decryption failed: Invalid token or key mismatch.")
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
