import re

import httpx
from nicegui import ui
from packaging.version import InvalidVersion, Version

from imxInsightsApps import __version__ as current_version
from imxInsightsApps.gui.settings import GITHUB_RELEASE_URL


async def fetch_newer_releases(include_pre_releases: bool = True):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(GITHUB_RELEASE_URL)
            response.raise_for_status()
            releases = response.json()

        current = Version(current_version)
        newer_releases = []

        for release in releases:
            tag = release["tag_name"].lstrip("v")
            try:
                release_version = Version(tag)
            except InvalidVersion:
                continue

            if release_version > current and (
                include_pre_releases or not release_version.is_prerelease
            ):
                newer_releases.append(
                    {
                        "version": str(release_version),
                        "notes": release["body"] or "No release notes provided.",
                        "url": release["html_url"],
                        "is_prerelease": release["prerelease"],
                    }
                )

    except Exception as e:
        ui.notify(f"Failed to check for updates: {e}", type="negative")
        return []
    else:
        return newer_releases


def normalize_markdown(notes: str) -> str:
    lines = notes.splitlines()
    cleaned = []

    for line in lines:
        # Remove lines with "by @user in https://..."
        if re.search(r"by\s+@\w[\w-]*\s+in\s+https?://\S+", line):
            line = "\n" + line.split("by @")[0] + "\n"

        # Replace markdown headers (## or ###) with bolded text
        line = re.sub(r"^(#{1,6})\s*(.+)", r"**\2**", line)

        if "Full Changelog" in line:
            continue

        cleaned.append(line)

    return "\n".join(cleaned).strip()


async def new_version_release_dialog(include_pre_releases: bool = True):
    releases = await fetch_newer_releases(include_pre_releases=include_pre_releases)
    if not releases:
        return

    normal_releases = [r for r in releases if not r["is_prerelease"]]
    prereleases = [r for r in releases if r["is_prerelease"]]

    with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl"):
        ui.label(f"New version{'s' if len(releases) > 1 else ''} available!").style(
            "color: #6E93D6; font-size: 200%; font-weight: 300"
        )

        if normal_releases:
            ui.label("Releases").classes("text-lg font-semibold mt-4")
            for r in normal_releases:
                with ui.row():
                    ui.label(f"Version {r['version']}")
                    ui.link("View on GitHub", r["url"], new_tab=True)
                ui.markdown(normalize_markdown(r["notes"]))

        if prereleases:
            ui.label("Pre-releases").classes("text-lg font-semibold mt-4")
            for r in prereleases:
                with ui.row():
                    ui.label(f"Version {r['version']} (pre-release)")
                    ui.link("View on GitHub", r["url"], new_tab=True)
                with ui.expansion("Notes").classes("w-full"):
                    ui.markdown(normalize_markdown(r["notes"]))

        ui.button("Close", on_click=dialog.close)

    dialog.open()
