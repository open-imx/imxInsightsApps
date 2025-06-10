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
            tag = release["tag_name"].lstrip("v")  # remove leading 'v'
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

        return newer_releases

    except Exception as e:
        ui.notify(f"Failed to check for updates: {e}", type="negative")
        return []


async def new_version_release_dialog(include_pre_releases: bool = True):
    releases = await fetch_newer_releases(include_pre_releases=include_pre_releases)
    if releases:
        with ui.dialog() as dialog, ui.card().classes("w-full max-w-2xl"):
            ui.label(
                f"New version{'s' if len(releases) > 1 else ''} available!"
            ).classes("text-xl font-bold")
            for r in releases:
                with ui.row():
                    label = f"Version {r['version']}"
                    if r["is_prerelease"]:
                        label += " (pre-release)"
                    ui.label(label)
                    ui.link("View on GitHub", r["url"], new_tab=True)

                ui.markdown(r["notes"])
            ui.button("Close", on_click=dialog.close)
        dialog.open()
