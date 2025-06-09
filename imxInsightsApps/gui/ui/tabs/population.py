from nicegui import run, ui

from imxInsightsApps.gui.logic.api_client import post_population
from imxInsightsApps.gui.logic.file_handlers import handle_upload
from imxInsightsApps.gui.logic.state_manager import get_client_id, init_tab_state
from imxInsightsApps.gui.settings import HIDDEN_BASE_DIR
from imxInsightsApps.gui.ui.components import (
    create_situation_select,
    create_upload_input,
)
from imxInsightsApps.gui.ui.helpers import reset_situation


def render_population_tab(spinner_dialog):
    client_id = get_client_id()
    state = init_tab_state("population")

    ui.markdown("""### 📊 Generate a population report from a IMX container.""")

    imx_situation = create_situation_select("📋 IMX Situation")
    create_upload_input(
        "📤 Upload IMX or ZIP",
        on_upload=lambda e: handle_upload(
            e, "imx", imx_situation, state, HIDDEN_BASE_DIR
        ),
        on_removed=lambda e: reset_situation("imx", imx_situation, state),
    )

    with ui.row():
        geojson_p = ui.checkbox("🗺️ Generate GeoJSON")
        to_wgs_p = ui.checkbox("🌐 Use WGS84 (EPSG:4326)").bind_visibility_from(
            geojson_p, "value"
        )

    async def run_population():
        try:
            if "imx" not in state["uploaded_files"]:
                ui.notify("⚠️ IMX file must be uploaded!", type="negative")
                return

            if (
                state["file_extensions"].get("imx") == ".xml"
                and not imx_situation.value
            ):
                ui.notify(
                    "⚠️ Situation must be selected for XML files.", type="negative"
                )
                return

            spinner_dialog.open()
            content, filename = await run.io_bound(
                post_population,
                state["uploaded_files"]["imx"],
                {
                    "situation": imx_situation.value or "",
                    "geojson": str(geojson_p.value).lower(),
                    "to_wgs": str(to_wgs_p.value).lower(),
                },
            )
            zip_path = HIDDEN_BASE_DIR / client_id / filename
            zip_path.write_bytes(content)
            ui.download(zip_path)
            ui.notify(
                f"✅ Population report completed! Downloading {filename} 📦",
                type="positive",
            )
            state["temp_files"].append(str(zip_path))
        except Exception as e:
            ui.notify(f"💥 Error during population: {e}", type="negative")
        finally:
            spinner_dialog.close()

    ui.button(
        "🧪 Create and download population report", on_click=run_population
    ).classes("mt-4 w-full")
