import subprocess
import platform

def connect_telnet(host, port, username, page):
    print(f"Попытка подключения к telnet {host}:{port} с пользователем {username}.")
    try:
        os_name = platform.system()

        if os_name == "Windows":
            command = f'putty -telnet {host} {port}'
            if username:
                command += f' -l {username}'
            # Пароль нельзя передать напрямую через командную строку PuTTY для Telnet

        elif os_name in ["Linux", "Darwin"]:
            command = f'telnet {host} {port}'

        else:
            print(f"Неизвестная операционная система: {os_name}. Подключение Telnet не поддерживается.")
            page.add(ft.Text(f"Неизвестная операционная система: {os_name}. Подключение Telnet не поддерживается."))
            return

        print(f"Выполняемая команда: {command}")
        subprocess.Popen(command, shell=True)  # Запускаем в новом процессе
        page.add(ft.Text(f"Подключение к Telnet {host}:{port} инициировано."))
    except Exception as e:
        print(f"Ошибка при подключении к Telnet: {e}")
        page.add(ft.Text(f"Ошибка при подключении к Telnet: {e}"))
