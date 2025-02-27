import flet as ft
import asyncio
import os
import platform
import subprocess

from config import (
    CONFIG_FILE,
    DEFAULT_PROTOCOL,
    SETTINGS_FILE,
    load_config,
    save_config,
)
from security import (
    encrypt_password,
    decrypt_password,
    is_encrypted,
)
from ui_module import show_confirmation_dialog
from rdp_module import connect_rdp
from telnet_module import connect_telnet

async def install_protocols_if_needed(page):
    """Устанавливает FreeRDP и TightVNC, если это необходимо и разрешено в настройках."""

    settings = load_config(SETTINGS_FILE)
    install_protocols = settings.get("install_protocols", True)

    if install_protocols:
        async def install_freerdp(page):
            print("Проверка наличия FreeRDP...")
            try:
                subprocess.run(["xfreerdp", "/version"], check=True, capture_output=True)
                print("FreeRDP уже установлен.")
                return True
            except FileNotFoundError:
                print("FreeRDP не найден. Попытка установки...")
                os_name = platform.system()

                try:
                    if os_name == "Windows":
                        print("Установка FreeRDP для Windows...")
                        # Пример: использование Chocolatey для установки
                        confirmation = await show_confirmation_dialog(page, "Установка FreeRDP",
                                                                     "Будет произведена попытка установки FreeRDP с использованием Chocolatey.  Продолжить?")
                        if not confirmation:
                            print("Установка FreeRDP отменена пользователем.")
                            return False

                        try:
                            subprocess.run(["choco", "install", "freerdp", "-y"], check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Ошибка при установке Chocolatey пакета: {e}")
                            page.add(ft.Text(f"Ошибка при установке Chocolatey пакета: {e}"))
                            return False
                        freerdp_path = "C:\\ProgramData\\chocolatey\\bin"  # Путь по умолчанию, может потребоваться проверка
                        os.environ["PATH"] += os.pathsep + freerdp_path
                        print("FreeRDP успешно установлен для Windows.")
                        page.add(ft.Text("FreeRDP успешно установлен для Windows."))
                    elif os_name == "Linux":
                        print("Установка FreeRDP для Linux...")
                        # Пример: установка через apt (для Debian/Ubuntu)
                        confirmation = await show_confirmation_dialog(page, "Установка FreeRDP",
                                                                     "Будет произведена попытка установки FreeRDP с использованием apt.  Продолжить?")
                        if not confirmation:
                            print("Установка FreeRDP отменена пользователем.")
                            return False
                        subprocess.run(["sudo", "apt", "install", "freerdp2-x11", "-y"], check=True)
                        print("FreeRDP успешно установлен для Linux.")
                        page.add(ft.Text("FreeRDP успешно установлен для Linux."))
                    elif os_name == "Darwin":  # macOS
                        print("Установка FreeRDP для macOS...")
                        # Пример: установка через brew
                        confirmation = await show_confirmation_dialog(page, "Установка FreeRDP",
                                                                     "Будет произведена попытка установки FreeRDP с использованием brew.  Продолжить?")
                        if not confirmation:
                            print("Установка FreeRDP отменена пользователем.")
                            return False
                        subprocess.run(["brew", "install", "freerdp"], check=True)
                        print("FreeRDP успешно установлен для macOS.")
                        page.add(ft.Text("FreeRDP успешно установлен для macOS."))
                    else:
                        print(
                            f"Неизвестная операционная система: {os_name}.  Установка FreeRDP не поддерживается автоматически.")
                        page.add(ft.Text(
                            f"Неизвестная операционная система: {os_name}. Установка FreeRDP не поддерживается автоматически."))
                        return False

                    print("FreeRDP установлен. Обновление переменной PATH...")
                    os.environ["PATH"] += os.pathsep + "/usr/local/bin"  # Пример пути для Linux/macOS
                    print("Переменная PATH обновлена.")
                    page.add(ft.Text("Переменная PATH обновлена."))

                    return True
                except subprocess.CalledProcessError as e:
                    print(f"Ошибка при установке FreeRDP: {e}")
                    page.add(ft.Text(f"Ошибка при установке FreeRDP: {e}"))
                    return False
                except Exception as e:
                    print(f"Непредвиденная ошибка при установке FreeRDP: {e}")
                    page.add(ft.Text(f"Непредвиденная ошибка при установке FreeRDP: {e}"))
                    return False

        async def install_tightvnc(page):
            print("Проверка наличия TightVNC...")
            try:
                subprocess.run(["tvnviewer", "-version"], check=True, capture_output=True)
                print("TightVNC уже установлен.")
                return True
            except FileNotFoundError:
                print("TightVNC не найден. Попытка установки...")
                os_name = platform.system()

                try:
                    if os_name == "Windows":
                        print("Установка TightVNC для Windows...")
                        confirmation = await show_confirmation_dialog(page, "Установка TightVNC",
                                                                     "Будет произведена попытка установки TightVNC с использованием Chocolatey.  Продолжить?")
                        if not confirmation:
                            print("Установка TightVNC отменена пользователем.")
                            return False
                        try:
                            subprocess.run(["choco", "install", "tightvnc", "-y"], check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Ошибка при установке Chocolatey пакета: {e}")
                            page.add(ft.Text(f"Ошибка при установке Chocolatey пакета: {e}"))
                            return False
                        tightvnc_path = "C:\\Program Files\\TightVNC"  # Путь по умолчанию, может потребоваться проверка
                        os.environ["PATH"] += os.pathsep + tightvnc_path
                        print("TightVNC успешно установлен для Windows.")
                        page.add(ft.Text("TightVNC успешно установлен для Windows."))
                    elif os_name == "Linux":
                        print("Установка TightVNC для Linux...")
                        confirmation = await show_confirmation_dialog(page, "Установка TightVNC",
                                                                     "Будет произведена попытка установки TightVNC с использованием apt.  Продолжить?")
                        if not confirmation:
                            print("Установка TightVNC отменена пользователем.")
                            return False
                        subprocess.run(["sudo", "apt", "install", "tightvncserver", "xtightvncviewer", "-y"], check=True)
                        print("TightVNC успешно установлен для Linux.")
                        page.add(ft.Text("TightVNC успешно установлен для Linux."))
                    elif os_name == "Darwin":  # macOS
                        print("Установка FreeRDP для macOS...")
                        confirmation = await show_confirmation_dialog(page, "Установка TightVNC",
                                                                     "Будет произведена попытка установки TightVNC с использованием brew.  Продолжить?")
                        if not confirmation:
                            print("Установка TightVNC отменена пользователем.")
                            return False
                        subprocess.run(["brew", "install", "tightvnc"], check=True)
                        print("FreeRDP успешно установлен для macOS.")
                        page.add(ft.Text("FreeRDP успешно установлен для macOS."))
                    else:
                        print(
                            f"Неизвестная операционная система: {os_name}. Установка TightVNC не поддерживается автоматически.")
                        page.add(ft.Text(
                            f"Неизвестная операционная система: {os_name}. Установка TightVNC не поддерживается автоматически."))
                        return False

                    print("TightVNC установлен. Обновление переменной PATH...")
                    os.environ["PATH"] += os.pathsep + "/usr/local/bin"  # Пример пути для Linux/macOS
                    print("Переменная PATH обновлена.")
                    page.add(ft.Text("Переменная PATH обновлена."))

                    return True
                except subprocess.CalledProcessError as e:
                    print(f"Ошибка при установке TightVNC: {e}")
                    page.add(ft.Text(f"Ошибка при установке TightVNC: {e}"))
                    return False
                except Exception as e:
                    print(f"Непредвиденная ошибка при установке TightVNC: {e}")
                    page.add(ft.Text(f"Непредвиденная ошибка при установке TightVNC: {e}"))
                    return False

        async def run_install():
            if not await install_freerdp(page):
                page.add(ft.Text("Не удалось установить FreeRDP.  Пожалуйста, установите его вручную."))
                return

            if not await install_tightvnc(page):
                page.add(ft.Text("Не удалось установить TightVNC.  Пожалуйста, установите его вручную."))
                return
        asyncio.create_task(run_install())

def load_connections():
    """Загружает подключения из файла конфигурации."""
    try:
        connections = load_config(CONFIG_FILE)
        print(f"Загружено {len(connections)} подключений.")
        return connections
    except Exception as e:
        print(f"Ошибка при загрузке подключений: {e}")
        return []

def save_connections(connections):
    """Сохраняет подключения в файл, шифруя пароли."""
    try:
        # Шифруем пароли перед сохранением
        for conn in connections:
            if 'password' in conn and conn['password'] and not is_encrypted(conn['password']):
                conn['password'] = encrypt_password(conn['password'])

        save_config(CONFIG_FILE, connections)
        print("Подключения успешно сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении подключений: {e}")

async def remove_connection(name, page, connections, rdp_tiles, telnet_tiles):
    """Удаляет подключение."""
    print(f"Удаление подключения: {name}.")

    confirmation = await show_confirmation_dialog(page, "Удаление подключения",
                                                 f"Вы уверены, что хотите удалить подключение '{name}'?")
    if confirmation:
        connections[:] = [conn for conn in connections if conn.get("name") != name]
        save_connections(connections)
        update_tiles(page, connections, rdp_tiles, telnet_tiles)
    else:
        print("Удаление подключения отменено пользователем.")

def update_tiles(page, connections, rdp_tiles, telnet_tiles, protocol=None):
    """Обновляет плитки подключений."""
    print("Обновление плиток для подключения.")
    rdp_tiles.controls.clear()
    telnet_tiles.controls.clear()

    rdp_tile_list = []
    telnet_tile_list = []

    # Сортируем подключения по имени
    rdp_connections = [conn for conn in connections if conn.get("protocol") != "telnet"]
    rdp_connections.sort(key=lambda x: x.get("name", "").lower())

    # Сортируем Telnet подключения по хосту
    telnet_connections = [conn for conn in connections if conn.get("protocol") == "telnet"]
    telnet_connections.sort(key=lambda x: x.get("host", "").lower())

    for conn in rdp_connections:
        if all(key in conn for key in ["name", "ip", "username"]):
            # Обработка RDP-подключения
            name = conn["name"]
            ip = conn["ip"]
            username = conn["username"]
            password = conn["password"]
            # Если протокол передан, используем его, иначе берем из настроек подключения, иначе дефолтный
            conn_protocol = protocol if protocol else conn.get("protocol", DEFAULT_PROTOCOL)

            popup_menu_button = ft.PopupMenuButton(
                icon=ft.Icons.MORE_HORIZ,
                tooltip="Конфигурация",
                items=[
                    ft.PopupMenuItem(
                        text="Изменить",
                        #on_click=lambda e, name=name: open_edit_window(name, page, connections, rdp_tiles, telnet_tiles) #TODO: Implement edit window
                    ),
                    ft.PopupMenuItem(
                        text="Удалить",
                        on_click=lambda e, name=name: asyncio.create_task(
                            remove_connection(name, page, connections, rdp_tiles, telnet_tiles))
                    ),
                ],
            )

            tile = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    popup_menu_button
                                ],
                                alignment=ft.MainAxisAlignment.END
                            ),
                            bgcolor="#272932",
                            height=30,
                            padding=0,
                            border_radius=ft.BorderRadius(
                                top_left=50,
                                top_right=50,
                                bottom_right=0,
                                bottom_left=50,
                            ),
                        ),
                        ft.ElevatedButton(
                            f"{name} ({conn_protocol})",  # Отображаем протокол в кнопке
                            height=100,
                            width=220,
                            on_click=lambda e, ip=ip, username=username, password=password, protocol=conn_protocol: connect_rdp(
                                ip, username, password, page, protocol),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(
                                    top_left=50,
                                    top_right=0,
                                    bottom_right=50,
                                    bottom_left=0,
                                ), ),
                                bgcolor="#272932"
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=220,
                padding=5,
            )

            rdp_tile_list.append(tile)

    for conn in telnet_connections:
        # Обработка Telnet-подключения
        host = conn.get("host")
        port = conn.get("port")
        username = conn.get("username")
        password = conn.get("password")
        conn_protocol = "telnet"  # Явно устанавливаем протокол telnet

        popup_menu_button = ft.PopupMenuButton(
            icon=ft.Icons.MORE_HORIZ,
            tooltip="Конфигурация",
            items=[
                ft.PopupMenuItem(
                    text="Изменить",
                    # on_click=lambda e, host=host: open_edit_telnet_window(host, page, connections, tiles)  # TODO: Implement edit window for Telnet
                ),
                ft.PopupMenuItem(
                    text="Удалить",
                    # on_click=lambda e, host=host: remove_connection(host, page, connections, tiles) # TODO: Implement remove connection for Telnet
                ),
            ],
        )

        tile = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                popup_menu_button
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        bgcolor="#272932",
                        height=30,
                        padding=0,
                        border_radius=ft.BorderRadius(
                            top_left=50,
                            top_right=50,
                            bottom_right=0,
                            bottom_left=50,
                        ),
                    ),
                    ft.ElevatedButton(
                        f"{host}:{port} ({conn_protocol})",  # Отображаем хост и порт в кнопке
                        height=100,
                        width=220,
                        on_click=lambda e, host=host, port=port, username=username, password=password: connect_telnet(
                            host, port, username, password, page),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(
                                top_left=50,
                                top_right=0,
                                bottom_right=50,
                                bottom_left=0,
                            ), ),
                            bgcolor="#272932"
                        )
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=220,
            padding=5,
        )
        telnet_tile_list.append(tile)

    rdp_tiles.controls.append(
        ft.Row(
            controls=rdp_tile_list,
            wrap=True,
            spacing=10,
            run_spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )

    telnet_tiles.controls.append(
        ft.Row(
            controls=telnet_tile_list,
            wrap=True,
            spacing=10,
            run_spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )
    page.update()

def open_add_window(page, connections, rdp_tiles, telnet_tiles, is_telnet=False):
    """Открывает окно добавления нового подключения."""
    print("Открытие окна добавления нового подключения.")

    if is_telnet:
        new_host_input = ft.TextField(label="IP адрес или имя хоста")
        new_port_input = ft.TextField(label="Порт", value="23")  # Default Telnet port
        new_username_input = ft.TextField(label="Имя пользователя")
        new_password_input = ft.TextField(label="Пароль", password=True)
        window_title = "Добавить новое Telnet подключение"
        window_content = ft.Column(
            controls=[new_host_input, new_port_input, new_username_input, new_password_input],
            spacing=10)
    else:
        new_name_input = ft.TextField(label="Название подключения")
        new_ip_input = ft.TextField(label="Адрес сервера")
        new_username_input = ft.TextField(label="Имя пользователя")
        new_password_input = ft.TextField(label="Пароль", password=True)
        protocol_dropdown = ft.Dropdown(
            label="Выберите протокол",
            value=load_protocol_from_config(),  # Текущий протокол из настроек
            options=[
                ft.DropdownOption("mstsc", "mstsc"),
                ft.DropdownOption("freerdp", "freerdp"),
                ft.DropdownOption("vnc", "vnc")
            ],
        )
        window_title = "Добавить новое RDP подключение"
        window_content = ft.Column(
            controls=[new_name_input, new_ip_input, new_username_input, new_password_input, protocol_dropdown],
            spacing=10)

    def close_add_window(e):
        print("Закрытие окна добавления.")
        page.dialog.open = False
        page.update()

    save_button = ft.ElevatedButton("Добавить подключение",
                                    on_click=lambda e: add_connection(
                                        *(
                                            (new_host_input, new_port_input, new_username_input, new_password_input)
                                            if is_telnet
                                            else (new_name_input, new_ip_input, new_username_input, new_password_input,
                                                  protocol_dropdown)
                                        ),
                                        page, connections, rdp_tiles, telnet_tiles, is_telnet
                                    ))
    cancel_button = ft.ElevatedButton("Отменить", on_click=close_add_window)

    def submit_add_window(e):
        add_connection(
            *(
                (new_host_input, new_port_input, new_username_input, new_password_input)
                if is_telnet
                else (new_name_input, new_ip_input, new_username_input, new_password_input, protocol_dropdown)
            ),
            page, connections, rdp_tiles, telnet_tiles, is_telnet
        )

    if not hasattr(page, "dialog"):
        page.dialog = ft.AlertDialog(
            title=ft.Text(window_title),
            content=window_content,
            actions=[save_button, cancel_button],
            on_dismiss=lambda e: print("Dialog was dismissed!"),
        )

    page.add(page.dialog)

    page.dialog.content = window_content
    page.dialog.open = True
    page.on_keyboard_event = lambda e: submit_add_window(e) if e.key == "Enter" else None
    page.update()

def add_connection(name_or_host_input, ip_or_port_input, username_input, password_input, page, connections, rdp_tiles,
                   telnet_tiles, is_telnet=False):
    """Добавляет новое подключение."""
    if is_telnet:
        new_host = name_or_host_input.value
        new_port = ip_or_port_input.value
        new_username = username_input.value
        new_password = password_input.value

        if new_host and new_port and new_username and new_password:
            print("Все поля для Telnet заполнены, добавляем подключение.")
            # Шифруем пароль перед добавлением в список
            encrypted_password = encrypt_password(new_password)
            new_connection = {
                "host": new_host,
                "port": new_port,
                "username": new_username,
                "password": encrypted_password,  # Сохраняем зашифрованный пароль
                "protocol": "telnet"  # Протокол для Telnet
            }

            connections.append(new_connection)
            save_connections(connections)
            update_tiles(page, connections, rdp_tiles, telnet_tiles)
            print("Telnet подключение добавлено.")
            page.dialog.open = False
            page.update()
        else:
            print("Не все поля для Telnet заполнены.")
            page.add(ft.Text("Все поля должны быть заполнены."))
    else:
        new_name = name_or_host_input.value
        new_ip = ip_or_port_input.value
        new_username = username_input.value
        new_password = password_input.value
        # protocol = load_protocol_from_config()  # Загружаем текущий протокол из конфигурации

        if new_name and new_ip and new_username and new_password:
            print("Все поля для RDP заполнены, добавляем подключение.")
            # Шифруем пароль перед добавлением в список
            encrypted_password = encrypt_password(new_password)
            new_connection = {
                "name": new_name,
                "ip": new_ip,
                "username": new_username,
                "password": encrypted_password,  # Сохраняем зашифрованный пароль
                "protocol": "mstsc"  # Протокол mstsc для RDP
            }
            connections.append(new_connection)
            save_connections(connections)
            update_tiles(page, connections, rdp_tiles, telnet_tiles)
            print("RDP подключение добавлено.")
            page.dialog.open = False
            page.update()
        else:
            print("Не все поля для RDP заполнены.")
            page.add(ft.Text("Все поля должны быть заполнены."))

def open_settings_window(page, main_container, settings_container, settings_tabs):
    """Открывает окно настроек."""
    print("Открытие окна настроек.")
    main_container.visible = False
    settings_container.visible = True
    page.update()

def close_settings_window(page, main_container, settings_container, protocol_dropdown, install_protocols_checkbox, connections, rdp_tiles, telnet_tiles):
    """Закрывает окно настроек и возвращается в главное меню."""
    print("Закрытие окна настроек, возвращение в главное меню.")
    settings_container.visible = False
    main_container.visible = True
    new_protocol = protocol_dropdown.value
    save_protocol_to_config(new_protocol)

    install_protocols = install_protocols_checkbox.value
    save_install_protocols_to_config(install_protocols)

    # Обновляем протокол для каждого подключения в списке connections
    for conn in connections:
        if conn.get('protocol') != 'telnet':
            conn['protocol'] = new_protocol
    save_connections(connections)  # Сохраняем изменения в connections.json

    page.update()
    update_tiles(page, connections, rdp_tiles, telnet_tiles, new_protocol)  # Передаем протокол для обновления плиток

def load_protocol_from_config():
    """Загружает протокол по умолчанию из файла конфигурации."""
    try:
        settings = load_config(SETTINGS_FILE)
        return settings.get("protocol", DEFAULT_PROTOCOL)
    except Exception:
        return DEFAULT_PROTOCOL

def load_install_protocols_from_config():
    """Загружает настройку установки протоколов из файла конфигурации."""
    try:
        settings = load_config(SETTINGS_FILE)
        return settings.get("install_protocols", True)
    except Exception:
        return True

def save_protocol_to_config(protocol):
    """Сохраняет протокол по умолчанию в файл конфигурации."""
    try:
        settings = load_config(SETTINGS_FILE)
        settings["protocol"] = protocol
        save_config(SETTINGS_FILE, settings)
        print(f"Протокол {protocol} сохранен в настройки.")
    except Exception as e:
        print(f"Ошибка при сохранении протокола: {e}")

def save_install_protocols_to_config(install_protocols):
    """Сохраняет настройку установки протоколов в файл конфигурации."""
    try:
        settings = load_config(SETTINGS_FILE)
        settings["install_protocols"] = install_protocols
        save_config(SETTINGS_FILE, settings)
        print(f"Настройка установки протоколов сохранена: {install_protocols}")
    except Exception as e:
        print(f"Ошибка при сохранении настройки установки протоколов: {e}")

async def main(page: ft.Page):
    """Основная функция приложения."""
    print("Запуск приложения.")
    page.title = "RDP Client Manager"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Установка протоколов, если это необходимо
    #create_taskinstall_protocols_if_needed(page)

    # Загрузка подключений и протокола
    connections = load_connections()
    protocol = load_protocol_from_config()

    # Контейнеры для кнопок и настроек
    rdp_header = ft.Row(
        controls=[
            ft.ElevatedButton(" + Добавить", on_click=lambda e: open_add_window(page, connections, rdp_tiles, telnet_tiles)),
            ft.IconButton(ft.Icons.SETTINGS,
                          on_click=lambda e: open_settings_window(page, main_container, settings_container, settings_tabs))
        ],
        alignment=ft.MainAxisAlignment.END
    )

    telnet_header = ft.Row(
        controls=[
            ft.ElevatedButton(" + Добавить", on_click=lambda e: open_add_window(page, connections, rdp_tiles, telnet_tiles, is_telnet=True)),
            ft.IconButton(ft.Icons.SETTINGS,
                          on_click=lambda e: open_settings_window(page, main_container, settings_container, settings_tabs))
        ],
        alignment=ft.MainAxisAlignment.END
    )

    # Контейнеры для основного контента и настроек
    rdp_tiles = ft.Column()
    telnet_tiles = ft.Column()
    main_container = ft.Column(controls=[], visible=True)
    settings_container = ft.Column(controls=[], visible=False)

    protocol_dropdown = ft.Dropdown(
        label="Выберите протокол",
        value=protocol,
        options=[
            ft.DropdownOption("mstsc", "mstsc"),
            ft.DropdownOption("freerdp", "freerdp"),
            ft.DropdownOption("vnc", "vnc")
        ],
    )

    install_protocols_checkbox = ft.Checkbox(
        label="Автоматически устанавливать FreeRDP и TightVNC",
        value=load_install_protocols_from_config(),
    )

    # Вкладки для главного меню
    main_tabs = ft.Tabs(
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="RDP",
                content=ft.Column([rdp_header, rdp_tiles])
            ),
            ft.Tab(
                text="Telnet",
                content=ft.Column([telnet_header, telnet_tiles])
            ),
        ],
        expand=1
    )

    # Вкладки для окна настроек
    settings_tabs = ft.Tabs(
        expand=True,
        animation_duration=300,
        label_color=ft.Colors.BLUE_GREY_900,
        unselected_label_color=ft.Colors.GREY_600,
        indicator_color=ft.Colors.BLUE_GREY_900,
        tabs=[
            ft.Tab(
                height=70,
                text="RDP",
                content=ft.Column([
                    ft.Text("Настройки для RDP"),
                    ft.Row([
                        ft.Text("Выберите протокол:"),
                        protocol_dropdown
                    ], alignment=ft.MainAxisAlignment.START),
                ])
            ),
            ft.Tab(
                height=70,
                text="Общие",
                content=ft.Column([
                    ft.Text("Общие настройки"),
                    ft.Row([
                        install_protocols_checkbox
                    ], alignment=ft.MainAxisAlignment.START),
                ])
            ),
        ],
    )

    def close_settings_window_event(e):
        close_settings_window(page, main_container, settings_container,
                              protocol_dropdown, install_protocols_checkbox, connections, rdp_tiles, telnet_tiles)

    settings_container.controls = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.ElevatedButton("Назад", on_click=close_settings_window_event),
                ft.Text("Настройки", size=20),
                ft.Container()  # Пустой контейнер для выравнивания
            ]
        ),
        settings_tabs,  # Добавляем вкладки настроек
    ]

    main_container.controls = [main_tabs]

    # Обработчик нажатия ESC
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Escape":
            if settings_container.visible:
                close_settings_window(page, main_container, settings_container,
                                      protocol_dropdown, install_protocols_checkbox, connections, rdp_tiles, telnet_tiles)
                page.update()

    page.on_keyboard_event = on_keyboard

    page.add(main_container, settings_container)

    update_tiles(page, connections, rdp_tiles, telnet_tiles)
    page.update()

ft.app(target=main)
