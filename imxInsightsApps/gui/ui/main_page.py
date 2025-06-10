import asyncio

from imxInsights import __version__ as insights_version
from nicegui import app, ui

from imxInsightsApps import __version__ as apps_version
from imxInsightsApps.gui.logic.app_version_check import new_version_release_dialog
from imxInsightsApps.gui.logic.state_manager import init_tab_state
from imxInsightsApps.gui.ui.components import (
    create_dark_mode_toggle,
    create_spinner_dialog,
)
from imxInsightsApps.gui.ui.tabs.diff import render_diff_tab
from imxInsightsApps.gui.ui.tabs.population import render_population_tab


@ui.page("/")
async def main_page():
    await new_version_release_dialog()
    init_tab_state("diff")
    init_tab_state("population")

    create_dark_mode_toggle()
    spinner_dialog = create_spinner_dialog()

    with ui.column().classes("items-left justify-left mt-6 w-full"):
        with ui.row():
            ui.label("ImxInsights.tools.gui").classes("text-3xl font-bold")
            ui.label(f"v{apps_version}").classes("text")

    with ui.tabs() as tabs:
        diff_tab = ui.tab("🔍 Diff")
        pop_tab = ui.tab("📊 Population")

    with ui.tab_panels(tabs, value=diff_tab).classes("w-full overflow-hidden"):
        with ui.tab_panel(diff_tab):
            render_diff_tab(spinner_dialog)
        with ui.tab_panel(pop_tab):
            render_population_tab(spinner_dialog)

    with ui.column().classes("items-center justify-center mt-6 w-full"):
        ui.label(f"⚙️ Powered by ImxInsights 🚀v{insights_version}").classes(
            "text-1xl font-bold"
        )
        with ui.row():
            ui.link("🌐 PyPI", target="https://pypi.org/project/imxInsights/").classes(
                "text-1xl font-bold text-blue-500 underline"
            )
            ui.link(
                "💻 GitHub", target="https://github.com/open-imx/imxInsights"
            ).classes("text-1xl font-bold text-blue-500 underline")
        ui.button("Shutdown backend", on_click=lambda: app.shutdown()).props(
            "color=red flat"
        ).classes("mt-4 text-lg font-bold")
