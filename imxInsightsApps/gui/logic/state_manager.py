from pathlib import Path
from typing import TypedDict

from nicegui import context


class TabState(TypedDict):
    uploaded_files: dict[str, Path]
    file_extensions: dict[str, str | None]
    temp_files: list[str]


client_states: dict[str, dict[str, TabState]] = {}


def get_client_id() -> str:
    return context.client.id


def init_tab_state(tab_key: str) -> TabState:
    client_id = get_client_id()
    if client_id not in client_states:
        client_states[client_id] = {}
    if tab_key not in client_states[client_id]:
        client_states[client_id][tab_key] = {
            "uploaded_files": {},
            "file_extensions": {},
            "temp_files": [],
        }
    return client_states[client_id][tab_key]
