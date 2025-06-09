import ctypes
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from imxInsights.file.singleFileImx.imxSituationEnum import ImxSituationEnum
from nicegui import ui

from imxInsightsApps.gui.logic.state_manager import get_client_id


def find_situations_in_xml(xml_file_path: Path) -> list[str]:
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        return [
            name
            for name in ImxSituationEnum.__members__
            if root.find(f".//{{*}}{name}") is not None
        ]
    except Exception as e:
        print(f"⚠️ Error parsing XML: {e}")
        return []


def make_hidden_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetFileAttributesW(str(path.resolve()), 0x02)


def handle_upload(e, label, situation_element, state, hidden_dir: Path):
    client_id = get_client_id()
    base_dir = hidden_dir / client_id / "uploads"
    base_dir.mkdir(parents=True, exist_ok=True)

    save_path = base_dir / f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{e.name}"
    with open(save_path, "wb") as f:
        f.write(e.content.read())

    state["uploaded_files"][label] = save_path
    state["file_extensions"][label] = save_path.suffix.lower()
    state["temp_files"].append(str(save_path))

    ext = save_path.suffix.lower()
    if ext == ".xml":
        situations = find_situations_in_xml(save_path)
        from ..ui.helpers import update_situation_select

        update_situation_select(situations, situation_element)
    else:
        situation_element.options, situation_element.value = [], ""
        situation_element.props("disable")

    ui.notify(f"📁 {label.upper()} uploaded: {save_path.name} 🎉", type="info")
