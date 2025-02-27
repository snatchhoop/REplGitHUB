import flet as ft
import asyncio

async def show_confirmation_dialog(page, title, content_text):
    """Отображает диалоговое окно подтверждения и возвращает True, если пользователь нажал "Да"."""
    confirmed = False
    close_dlg = lambda e: page.close_dialog()

    async def yes_click(e):
        nonlocal confirmed
        confirmed = True
        page.close_dialog()

    async def no_click(e):
        nonlocal confirmed
        confirmed = False
        page.close_dialog()

    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(content_text),
        actions=[
            ft.TextButton("Да", on_click=yes_click),
            ft.TextButton("Нет", on_click=no_click),
        ],
        on_dismiss=close_dlg,
    )
    page.open_dialog(page.dialog)
    await page.update_async()

    # Ждем, пока диалог не будет закрыт
    while page.dialog.open:
        await asyncio.sleep(0.1)  # Небольшая задержка, чтобы избежать блокировки
        await page.update_async()

    return confirmed
