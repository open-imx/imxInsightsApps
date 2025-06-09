import shutil
from pathlib import Path

from nicegui import context

from imxInsightsApps.gui.logic.state_manager import client_states

HIDDEN_BASE_DIR = Path(".temp_data")


def setup_hidden_base_dir():
    from .file_handlers import make_hidden_dir

    make_hidden_dir(HIDDEN_BASE_DIR)


def cleanup_user_temp_files():
    client_id = context.client.id
    state = client_states.pop(client_id, None)
    client_root = HIDDEN_BASE_DIR / client_id

    base_dirs = [
        client_root / "uploads",
        client_root / "output",
        client_root / "work",
    ]

    if state:
        for tab_state in state.values():
            for path_str in tab_state.get("temp_files", []):
                try:
                    path = Path(path_str)
                    if path.is_dir():
                        shutil.rmtree(path, ignore_errors=True)
                    elif path.is_file():
                        path.unlink(missing_ok=True)
                except Exception as e:
                    print(f"⚠️ Error deleting {path_str}: {e}")

    for folder in base_dirs:
        try:
            shutil.rmtree(folder, ignore_errors=True)
        except Exception as e:
            print(f"⚠️ Error deleting folder {folder}: {e}")

    try:
        if client_root.exists() and not any(client_root.iterdir()):
            client_root.rmdir()
    except Exception as e:
        print(f"⚠️ Error deleting client root folder {client_root}: {e}")


def cleanup_temp_files():
    print("🧹 Global cleanup on shutdown...")
    if HIDDEN_BASE_DIR.exists():
        for folder in HIDDEN_BASE_DIR.glob("*"):
            shutil.rmtree(folder, ignore_errors=True)
