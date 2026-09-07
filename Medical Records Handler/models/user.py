import uuid
from crypto.digital_signature import generate_key_pair
from cryptography.hazmat.primitives import serialization
from utils.file_utils import load_json_file, save_json_file, get_file_path


class UserBase:
    def __init__(self, name, role, hospital_id=None, insurance_id=None,tokens=0):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.hospital_id = hospital_id
        self.insurance_id = insurance_id
        self.private_key = None
        self.public_key = None
        self.tokens = tokens

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "hospital_id": self.hospital_id,
            "insurance_id": self.insurance_id,
            "tokens": self.tokens
        }

    def to_dict_with_keypair(self):
        if self.private_key is None or self.public_key is None:
            self.private_key, self.public_key = generate_key_pair()
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        d = self.to_dict()
        d['public_key'] = public_pem
        return d, self.private_key

    @classmethod
    def from_dict(cls, data):
        obj = cls(data["name"], data["role"], data.get(
            "hospital_id"), data.get("insurance_id"))
        obj.user_id = data["user_id"]
        return obj


class Patient(UserBase):
    def __init__(self, name, insurance_id=None):
        super().__init__(name, "patient", insurance_id=insurance_id)


class Doctor(UserBase):
    def __init__(self, name, hospital_id=None):
        super().__init__(name, "doctor", hospital_id=hospital_id,tokens=25)

    def can_modify_record(self, consent):
        return consent


class Administrator(UserBase):
    def __init__(self, name, hospital_id=None):
        super().__init__(name, "admin", hospital_id=hospital_id,tokens=50)
