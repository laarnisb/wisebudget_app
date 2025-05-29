from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import os

# Constants
BLOCK_SIZE = AES.block_size  # 16 bytes
KEY_LENGTH = 32  # 256 bits
SALT = b'static_salt_value'  # In production, use os.urandom(16) and store with the ciphertext
SECRET_PASSPHRASE = os.getenv("AES_PASSPHRASE", "default_passphrase")

def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + chr(pad_len) * pad_len

def unpad(data):
    pad_len = ord(data[-1])
    return data[:-pad_len]

def derive_key(passphrase: str, salt: bytes) -> bytes:
    return PBKDF2(passphrase, salt, dkLen=KEY_LENGTH)

def encrypt_data(data: str) -> str:
    key = derive_key(SECRET_PASSPHRASE, SALT)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data).encode()
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode()

def decrypt_data(encrypted_data: str) -> str:
    key = derive_key(SECRET_PASSPHRASE, SALT)
    raw = base64.b64decode(encrypted_data)
    iv = raw[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(raw[BLOCK_SIZE:]).decode()
    return unpad(decrypted)
