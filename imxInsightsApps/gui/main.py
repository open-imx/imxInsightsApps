import ctypes
import shutil
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
from imxInsights import __version__ as insights_version
from imxInsights.file.singleFileImx.imxSituationEnum import ImxSituationEnum
from nicegui import app, context, native, run, ui

from imxInsightsApps.api.main import api_app
from imxInsightsApps import __version__ as apps_version

# we make a test client to call endpoints
client = TestClient(api_app)

client_states = {}

HIDDEN_BASE_DIR = Path(".temp_data")


def make_hidden_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(str(path.resolve()), FILE_ATTRIBUTE_HIDDEN)


make_hidden_dir(HIDDEN_BASE_DIR)


def find_situations_in_xml(xml_file_path: Path) -> list[str]:
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        return [name for name in ImxSituationEnum.__members__ if root.find(f".//{{*}}{name}") is not None]
    except Exception as e:
        print(f"⚠️ Error parsing XML: {e}")
        return []


def get_situation_enum(value: str | None):
    return ImxSituationEnum(value) if value else None


def handle_upload(e, label, situation_element, state):
    client_id = context.client.id
    base_dir = HIDDEN_BASE_DIR / client_id / "uploads"
    base_dir.mkdir(parents=True, exist_ok=True)

    save_path = base_dir / f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{e.name}"
    with open(save_path, "wb") as f:
        f.write(e.content.read())

    state["uploaded_files"][label] = save_path
    state["file_extensions"][label] = save_path.suffix.lower()
    state["temp_files"].append(str(save_path))

    ext = state["file_extensions"][label]
    if ext == ".xml":
        situations = find_situations_in_xml(save_path)
        update_situation_select(situations, situation_element)
    else:
        situation_element.options, situation_element.value = [], ""
        situation_element.props("disable")

    ui.notify(f"📁 {label.upper()} uploaded: {save_path.name} 🎉", type="info")


def update_situation_select(situations, element):
    if situations:
        element.options = situations
        element.props(remove="disable")
        if len(situations) == 1:
            element.value = situations[0]
            ui.notify(f"🧠 Auto-detected situation: {situations[0]}", type="info")
        else:
            element.value = ""
            ui.notify(f"🧠 Multiple situations found: {', '.join(situations)}", type="info")
    else:
        element.options, element.value = [], ""
        element.props(remove="disable")
        ui.notify("❓ No known situation elements found in XML.", type="warning")


def reset_situation(label: str, situation_element, state):
    state["uploaded_files"].pop(label, None)
    state["file_extensions"][label] = None
    situation_element.value = ""
    situation_element.props("disable")
    ui.notify(f"🗑️ {label.upper()} file removed. Situation reset.", type="warning")


@app.on_startup
def setup_hidden_base_dir():
    make_hidden_dir(HIDDEN_BASE_DIR)


@app.on_disconnect
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


@app.on_shutdown
def cleanup_temp_files():
    print("🧹 Global cleanup on shutdown...")
    if HIDDEN_BASE_DIR.exists():
        for folder in HIDDEN_BASE_DIR.glob("*"):
            shutil.rmtree(folder, ignore_errors=True)


@ui.page("/")
def main_page():
    client_id = context.client.id
    if client_id not in client_states:
        client_states[client_id] = {}

    dark_mode = ui.dark_mode()
    dark_mode.enable()

    def toggle_dark_light():
        dark_mode.toggle()
        toggle_button.text = "🔦" if dark_mode.value else "🌙"

    global toggle_button
    toggle_button = ui.button(
        "🔦" if dark_mode.value else "🌙",
        color=None,
        on_click=toggle_dark_light,
    ).classes("absolute top-4 right-4 border-0 outline-none ring-0 shadow-none z-50")

    def init_tab_state(tab_key: str):
        if tab_key not in client_states[client_id]:
            client_states[client_id][tab_key] = {
                "uploaded_files": {},
                "file_extensions": {},
                "temp_files": [],
            }
        return client_states[client_id][tab_key]

    with ui.dialog() as spinner_dialog, ui.card().classes("p-8 items-center"):
        ui.spinner(size="lg").props("color=primary")
        ui.label("⏳ Processing, please wait... 🛠️").classes("mt-4")

    with ui.column().classes("items-left justify-left mt-6 w-full"):
        with ui.row():
            ui.label("ImxInsights.tools.gui").classes("text-3xl font-bold")
            ui.label(f"v{apps_version}").classes("text")

    with ui.tabs() as tabs:
        diff_tab = ui.tab("🔍 Diff")
        pop_tab = ui.tab("📊 Population")

    with ui.tab_panels(tabs, value=diff_tab).classes("w-full overflow-hidden"):
        with ui.tab_panel(diff_tab):
            state = init_tab_state("diff")
            ui.markdown("""### 🔍 Compare IMX Containers and generate a diff report.""")

            upload_t1 = ui.upload(
                label="📤 Upload T1 IMX or ZIP",
                auto_upload=True,
                on_upload=lambda e: handle_upload(e, "t1", t1_situation, state),
            ).classes("w-full")

            t1_situation = ui.select([], label="🧾 T1 Situation").props("disable").classes("w-full")
            upload_t1.on("removed", lambda e: reset_situation("t1", t1_situation, state))

            upload_t2 = ui.upload(
                label="📤 Upload T2 IMX or ZIP",
                auto_upload=True,
                on_upload=lambda e: handle_upload(e, "t2", t2_situation, state),
            ).classes("w-full")

            t2_situation = ui.select([], label="🧾 T2 Situation").props("disable").classes("w-full")
            upload_t2.on("removed", lambda e: reset_situation("t2", t2_situation, state))

            with ui.row():
                geojson = ui.checkbox("🗺️ Generate GeoJSON")
                to_wgs = ui.checkbox("🌐 Use WGS84 (EPSG:4326)").bind_visibility_from(geojson, "value")

            version_checkbox = ui.checkbox("🆚 Compare across IMX versions", value=False)

            async def run_diff():
                if "t1" not in state["uploaded_files"] or "t2" not in state["uploaded_files"]:
                    ui.notify("⚠️ Both T1 and T2 files must be uploaded!", type="negative")
                    return

                if state["file_extensions"].get("t1") == ".xml" and not t1_situation.value:
                    ui.notify("⚠️ T1 situation must be selected for XML files.", type="negative")
                    return

                if state["file_extensions"].get("t2") == ".xml" and not t2_situation.value:
                    ui.notify("⚠️ T2 situation must be selected for XML files.", type="negative")
                    return

                spinner_dialog.open()
                try:
                    with open(state["uploaded_files"]["t1"], "rb") as t1, open(
                        state["uploaded_files"]["t2"], "rb"
                    ) as t2:
                        response = await run.io_bound(
                            client.post,
                            "/diff",
                            files={
                                "t1_file": ("t1.xml", t1),
                                "t2_file": ("t2.xml", t2),
                            },
                            data={
                                "t1_situation": t1_situation.value or "",
                                "t2_situation": t2_situation.value or "",
                                "geojson": str(geojson.value).lower(),
                                "to_wgs": str(to_wgs.value).lower(),
                                "compare_versions": str(version_checkbox.value).lower(),
                            },
                        )

                        if response.status_code != 200:
                            raise Exception(f"API error: {response.text}")

                        content_disp = response.headers.get("content-disposition", "")
                        filename = "diff_result.zip"
                        if "filename=" in content_disp:
                            filename = content_disp.split("filename=")[-1].strip('"')

                        zip_path = HIDDEN_BASE_DIR / client_id / filename
                        zip_path.write_bytes(response.content)

                        ui.download(zip_path)
                        ui.notify(f"✅ Diff completed! Downloading {filename} 📦", type="positive")
                        state["temp_files"].append(str(zip_path))

                        shutil.rmtree(HIDDEN_BASE_DIR / client_id / "uploads", ignore_errors=True)

                except Exception as e:
                    ui.notify(f"💥 Error during diff: {e}", type="negative")
                finally:
                    spinner_dialog.close()

            ui.button("🧪 Create and download diff report", on_click=run_diff).classes("mt-4 w-full")

        with ui.tab_panel(pop_tab):
            state = init_tab_state("population")
            ui.markdown("""### 📊 Generate a population report from a IMX container.""")

            upload_imx = ui.upload(
                label="📤 Upload IMX or ZIP",
                auto_upload=True,
                on_upload=lambda e: handle_upload(e, "imx", imx_situation, state),
            ).classes("w-full")
            upload_imx.on("removed", lambda e: reset_situation("imx", imx_situation, state))

            imx_situation = ui.select([], label="📋 IMX Situation").classes("w-full")

            with ui.row():
                geojson_p = ui.checkbox("🗺️ Generate GeoJSON")
                to_wgs_p = ui.checkbox("🌐 Use WGS84 (EPSG:4326)").bind_visibility_from(geojson_p, "value")

            async def run_population():
                if "imx" not in state["uploaded_files"]:
                    ui.notify("⚠️ IMX file must be uploaded!", type="negative")
                    return

                if state["file_extensions"].get("imx") == ".xml" and not imx_situation.value:
                    ui.notify("⚠️ Situation must be selected for XML files.", type="negative")
                    return

                spinner_dialog.open()
                try:
                    with open(state["uploaded_files"]["imx"], "rb") as imx:
                        response = await run.io_bound(
                            client.post,
                            "/population",
                            files={"imx_file": ("imx.xml", imx)},
                            data={
                                "situation": imx_situation.value or "",
                                "geojson": str(geojson_p.value).lower(),
                                "to_wgs": str(to_wgs_p.value).lower(),
                            },
                        )

                        if response.status_code != 200:
                            raise Exception(f"API error: {response.text}")

                        content_disp = response.headers.get("content-disposition", "")
                        filename = "population_result.zip"
                        if "filename=" in content_disp:
                            filename = content_disp.split("filename=")[-1].strip('"')

                        zip_path = HIDDEN_BASE_DIR / client_id / filename
                        zip_path.write_bytes(response.content)

                        ui.download(zip_path)
                        ui.notify(f"✅ Population report completed! Downloading {filename} 📦", type="positive")
                        state["temp_files"].append(str(zip_path))

                        shutil.rmtree(HIDDEN_BASE_DIR / client_id / "uploads", ignore_errors=True)

                except Exception as e:
                    ui.notify(f"💥 Error during population: {e}", type="negative")
                finally:
                    spinner_dialog.close()

            ui.button("🧪 Create and download population report", on_click=run_population).classes("mt-4 w-full")

    with ui.column().classes("items-center justify-center mt-6 w-full"):
        ui.label(f"⚙️ Powered by ImxInsights 🚀v{insights_version}").classes("text-1xl font-bold")
        with ui.row():
            ui.link("🌐 PyPI", target="https://pypi.org/project/imxInsights/").classes("text-1xl font-bold text-blue-500 underline")
            ui.link("💻 GitHub", target="https://github.com/open-imx/imxInsights").classes("text-1xl font-bold text-blue-500 underline")
        ui.button("Shutdown backend", on_click=lambda: app.shutdown()).props("color=red flat").classes("mt-4 text-lg font-bold")


app.include_router(api_app.router)

if __name__ == "__main__":
    is_frozen = getattr(sys, "frozen", False)
    chosen_port = 8003 if is_frozen else native.find_open_port()

    ui.run(
        reload=False,
        port=chosen_port,
        title="ImxInsights.app",
        dark=True,
        fastapi_docs=True,
    )
