from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from crypto.hashing import create_hash
from cryptography.exceptions import InvalidSignature

# Generate ECDSA key pair for encrypting digital signatures
def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key

# Sign data using the private key
def sign_data(private_key, trans_data):
    trans_hash = create_hash(trans_data)
    trans_hash_bytes = trans_hash.encode()
    signature = private_key.sign(
        trans_hash_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

# Verify digital signature using the public key
def verify_signature(public_key, signature, trans_data):
    trans_hash_bytes = create_hash(trans_data).encode()
    try:
        public_key.verify(
            signature,
            trans_hash_bytes,
            ec.ECDSA(hashes.SHA256())
        )
    except InvalidSignature:
        return False
    return True
