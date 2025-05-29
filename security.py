from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import os

# Pad and unpad functions for block size compliance
BS = AES.block_size

def pad(s):
    padding_length = BS - len(s) % BS
    return s + (chr(padding_length) * padding_length).encode()

def unpad(s):
    return s[:-s[-1]]

# Generate a new encryption key (only once, store securely)
def generate_key():
    return base64.urlsafe_b64encode(get_random_bytes(32)).decode()

# Encrypt data using AES-256-CBC
def encrypt_data(data, key):
    key_bytes = base64.urlsafe_b64decode(key.encode())
    iv = get_random_bytes(BS)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode()))
    return base64.b64encode(iv + encrypted).decode()

# Decrypt data
def decrypt_data(encrypted_data, key):
    key_bytes = base64.urlsafe_b64decode(key.encode())
    encrypted_data_bytes = base64.b64decode(encrypted_data.encode())
    iv = encrypted_data_bytes[:BS]
    encrypted = encrypted_data_bytes[BS:]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted))
    return decrypted.decode()
