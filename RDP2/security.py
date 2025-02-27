from cryptography.fernet import Fernet
import os
from config import KEY_FILE

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"Сгенерирован новый ключ: {key}")
    return key

def load_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
            print(f"Ключ загружен из файла: {key}")
            return key
    except FileNotFoundError:
        print("Файл с ключом не найден, генерируем новый.")
        return generate_key()

key = load_key()
fernet = Fernet(key)

def encrypt_password(password):
    print(f"Шифруем пароль: {password}")
    encrypted_password = fernet.encrypt(password.encode()).decode()
    print(f"Зашифрованный пароль: {encrypted_password}")
    return encrypted_password

def decrypt_password(encrypted_password):
    print(f"Дешифруем пароль: {encrypted_password}")
    decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
    print(f"Дешифрованный пароль: {decrypted_password}")
    return decrypted_password

def is_encrypted(password):
    if not isinstance(password, str):
        return False
    try:
        decrypt_password(password)
        return True
    except:
        return False
