import os
import sys

import sentry_sdk
from dotenv import load_dotenv
from nicegui import app, native, ui
from sentry_sdk.integrations.fastapi import FastApiIntegration

from imxInsightsApps.api.main import api_app
from imxInsightsApps.gui.logic.cleanup import (
    cleanup_temp_files,
    cleanup_user_temp_files,
    setup_hidden_base_dir,
)
from imxInsightsApps.gui.ui.main_page import main_page

load_dotenv()

sentry_sdk.init(
    integrations=[FastApiIntegration()],
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
    traces_sample_rate=1.0,
)

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
