from collections.abc import Callable

from nicegui import ui
from nicegui.elements.select import Select


def create_upload_input(
    label: str, on_upload: Callable, on_removed: Callable | None = None
):
    upload = ui.upload(
        label=label,
        auto_upload=True,
        on_upload=on_upload,
    ).classes("w-full")

    if on_removed:
        upload.on("removed", on_removed)

    return upload


def create_situation_select(label: str) -> Select:
    return ui.select([], label=label).props("disable").classes("w-full")


def create_spinner_dialog():
    with (
        ui.dialog().props("persistent") as dialog,
        ui.card().classes("p-8 items-center"),
    ):
        ui.spinner(size="lg").props("color=primary")
        ui.label("⏳ Processing, please wait... 🛠️").classes("mt-4")
    return dialog


def create_dark_mode_toggle():
    dark_mode = ui.dark_mode()
    dark_mode.enable()

    def toggle_dark_light():
        dark_mode.toggle()
        toggle_button.text = "🔦" if dark_mode.value else "🌙"

    toggle_button = ui.button(
        "🔦" if dark_mode.value else "🌙",
        color=None,
        on_click=toggle_dark_light,
    ).classes("absolute top-4 right-4 border-0 outline-none ring-0 shadow-none z-50")

    return toggle_button
