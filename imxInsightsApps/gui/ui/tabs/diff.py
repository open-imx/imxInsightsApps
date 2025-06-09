from nicegui import run, ui

from imxInsightsApps.gui.logic.api_client import post_diff
from imxInsightsApps.gui.logic.file_handlers import handle_upload
from imxInsightsApps.gui.logic.state_manager import get_client_id, init_tab_state
from imxInsightsApps.gui.settings import HIDDEN_BASE_DIR
from imxInsightsApps.gui.ui.components import (
    create_situation_select,
    create_upload_input,
)
from imxInsightsApps.gui.ui.helpers import reset_situation


def render_diff_tab(spinner_dialog):
    client_id = get_client_id()
    state = init_tab_state("diff")

    ui.markdown("""### 🔍 Compare IMX Containers and generate a diff report.""")

    t1_situation = create_situation_select("🧾 T1 Situation")
    create_upload_input(
        "📤 Upload T1 IMX or ZIP",
        on_upload=lambda e: handle_upload(
            e, "t1", t1_situation, state, HIDDEN_BASE_DIR
        ),
        on_removed=lambda e: reset_situation("t1", t1_situation, state),
    )

    t2_situation = create_situation_select("🧾 T2 Situation")
    create_upload_input(
        "📤 Upload T2 IMX or ZIP",
        on_upload=lambda e: handle_upload(
            e, "t2", t2_situation, state, HIDDEN_BASE_DIR
        ),
        on_removed=lambda e: reset_situation("t2", t2_situation, state),
    )

    with ui.row():
        geojson = ui.checkbox("🗺️ Generate GeoJSON")
        to_wgs = ui.checkbox("🌐 Use WGS84 (EPSG:4326)").bind_visibility_from(
            geojson, "value"
        )

    version_checkbox = ui.checkbox("🆚 Compare across IMX versions", value=False)

    async def run_diff():
        try:
            if (
                "t1" not in state["uploaded_files"]
                or "t2" not in state["uploaded_files"]
            ):
                ui.notify("⚠️ Both T1 and T2 files must be uploaded!", type="negative")
                return

            if state["file_extensions"].get("t1") == ".xml" and not t1_situation.value:
                ui.notify(
                    "⚠️ T1 situation must be selected for XML files.", type="negative"
                )
                return

            if state["file_extensions"].get("t2") == ".xml" and not t2_situation.value:
                ui.notify(
                    "⚠️ T2 situation must be selected for XML files.", type="negative"
                )
                return

            spinner_dialog.open()
            content, filename = await run.io_bound(
                post_diff,
                state["uploaded_files"]["t1"],
                state["uploaded_files"]["t2"],
                {
                    "t1_situation": t1_situation.value or "",
                    "t2_situation": t2_situation.value or "",
                    "geojson": str(geojson.value).lower(),
                    "to_wgs": str(to_wgs.value).lower(),
                    "compare_versions": str(version_checkbox.value).lower(),
                },
            )
            zip_path = HIDDEN_BASE_DIR / client_id / filename
            zip_path.write_bytes(content)
            ui.download(zip_path)
            ui.notify(f"✅ Diff completed! Downloading {filename} 📦", type="positive")
            state["temp_files"].append(str(zip_path))
        except Exception as e:
            ui.notify(f"💥 Error during diff: {e}", type="negative")
        finally:
            spinner_dialog.close()

    ui.button("🧪 Create and download diff report", on_click=run_diff).classes(
        "mt-4 w-full"
    )
