import os
import json

CONFIG_DIR = os.path.join(os.getcwd(), "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "connections.json")
DEFAULT_PROTOCOL = "mstsc"
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")
TELNET_SETTINGS_FILE = os.path.join(CONFIG_DIR, "telnet_settings.json")
KEY_FILE = os.path.join(CONFIG_DIR, "secret.key")

# Создаем директорию, если она не существует
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

def load_config(file_path):
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_config(file_path, config_data):
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении конфигурации: {e}")
