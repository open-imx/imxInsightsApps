import sys

from nicegui import app, native, ui

from imxInsightsApps.api.main import api_app
from imxInsightsApps.gui.logic.cleanup import (
    cleanup_temp_files,
    cleanup_user_temp_files,
    setup_hidden_base_dir,
)
from imxInsightsApps.gui.ui.main_page import main_page

app.on_startup(setup_hidden_base_dir)
app.on_disconnect(cleanup_user_temp_files)
app.on_shutdown(cleanup_temp_files)
app.include_router(api_app.router)

main_page()


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
