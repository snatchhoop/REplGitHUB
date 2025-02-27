import subprocess
import os
import platform
from config import DEFAULT_PROTOCOL
import security

def is_rdp_connected():
    # Проверка на наличие активных RDP-сессий
    result = subprocess.run('query', shell=True, capture_output=True, text=True)
    return "rdp-tcp" in result.stdout

def connect_rdp(ip, username, password, page, protocol=DEFAULT_PROTOCOL):
    print(f"Попытка подключения к {ip} с пользователем {username}. Используется протокол: {protocol}.")
    try:
        if protocol == "mstsc":
            if is_rdp_connected():
                subprocess.run(f'mstsc /v:{ip}', shell=True, check=True)
                page.add(ft.Text("Подключение к {ip} через mstsc."))
            else:
                rdp_file_content = f"full address:s:{ip}\nusername:s:{username}"
                rdp_file_path = os.path.join(os.path.dirname(__file__), "connection.rdp")

                with open(rdp_file_path, "w") as rdp_file:
                    rdp_file.write(rdp_file_content)

                command = f'mstsc "{rdp_file_path}" /f'
                subprocess.run(command, shell=True, check=True)

        elif protocol == "freerdp":
            xfreerdp_path = "C:\\ProgramData\\chocolatey\\bin\\xfreerdp.exe"  # Пример пути

            if os.path.exists(xfreerdp_path):
                command = f'"{xfreerdp_path}" /v:{ip} /u:{username} /p:{password} /f'
                subprocess.run(command, shell=True, check=True)
            else:
                print(f"Файл xfreerdp не найден по пути: {xfreerdp_path}")
                page.add(ft.Text("Файл xfreerdp не найден по пути: {xfreerdp_path}"))
                return
        elif protocol == "vnc":
            vncviewer_path = "C:\\Program Files\\TightVNC\\tvnviewer.exe"

            if os.path.exists(vncviewer_path):
                command = f'"{vncviewer_path}" -connect {ip}'
                if username:  # Добавляем имя пользователя, если оно указано
                    command += f' -username {username}'
                command += f' -password {password}'

                try:
                    os.startfile(vncviewer_path, parameters=f'-connect {ip} -username {username} -password {password}')
                except Exception as e:
                    print(f"Ошибка при запуске tvnviewer: {e}")
                    page.add(ft.Text("Ошибка при запуске tvnviewer: {e}"))
            else:
                print(f"Файл tvnviewer не найден по пути: {vncviewer_path}")
                page.add(ft.Text("Файл tvnviewer не найден по пути: {vncviewer_path}"))
                return

        print(f"Успешное подключение к {ip} с протоколом {protocol}!")
        page.add(ft.Text("Подключение к {ip} через {protocol}."))
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при подключении: {e}")
        page.add(ft.Text("Ошибка при подключении: {e}"))
