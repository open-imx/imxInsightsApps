import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from imxInsights import __version__ as insights_version
from imxInsights.file.singleFileImx.imxSituationEnum import ImxSituationEnum

from imxInsightsApps import __version__ as apps_version
from imxInsightsApps.shared.diff_and_population import (
    write_diff_output_files,
    write_population_output_files,
)

description = f"""
Using [imxInsights {insights_version}](https://pypi.org/project/imxInsights/)  
"""

api_app = FastAPI(
    title="ImxInsights tools API", description=description, version=apps_version
)

BASE_DIR = Path(tempfile.gettempdir()) / "imx_api"
BASE_DIR.mkdir(exist_ok=True)


def zip_output_folder(output_path: Path) -> Path:
    zip_path = output_path.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in output_path.rglob("*"):
            if file.is_file():
                zipf.write(file, file.relative_to(output_path))
    return zip_path


def get_situation_enum(value: str | None):
    return ImxSituationEnum(value) if value else None


@api_app.post("/diff")
async def create_diff(
    t1_file: UploadFile = File(...),
    t2_file: UploadFile = File(...),
    t1_situation: ImxSituationEnum = Form(None),
    t2_situation: ImxSituationEnum = Form(None),
    geojson: bool = Form(False),
    to_wgs: bool = Form(False),
    compare_versions: bool = Form(False),
):
    work_dir = BASE_DIR / f"diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    work_dir.mkdir(parents=True, exist_ok=True)

    if t1_file.filename is None:
        raise ValueError("t1 imx should have a filename")
    if t2_file.filename is None:
        raise ValueError("t2 imx should have a filename")

    t1_path = work_dir / t1_file.filename
    t2_path = work_dir / t2_file.filename

    t1_path.write_bytes(await t1_file.read())
    t2_path.write_bytes(await t2_file.read())

    write_diff_output_files(
        t1_path,
        t2_path,
        work_dir,
        get_situation_enum(t1_situation),
        get_situation_enum(t2_situation),
        geojson,
        to_wgs,
        compare_versions,
    )

    t1_path.unlink(missing_ok=True)
    t2_path.unlink(missing_ok=True)

    zip_path = zip_output_folder(work_dir)
    return FileResponse(zip_path, filename=zip_path.name, media_type="application/zip")


@api_app.post("/population")
async def create_population(
    imx_file: UploadFile = File(...),
    situation: ImxSituationEnum = Form(None),
    geojson: bool = Form(False),
    to_wgs: bool = Form(False),
):
    work_dir = BASE_DIR / f"pop_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    work_dir.mkdir(parents=True, exist_ok=True)
    if imx_file.filename is None:
        raise ValueError("imx should have a filename")

    imx_path = work_dir / imx_file.filename
    imx_path.write_bytes(await imx_file.read())

    write_population_output_files(
        imx_path,
        work_dir,
        get_situation_enum(situation),
        geojson,
        to_wgs,
    )

    imx_path.unlink(missing_ok=True)

    zip_path = zip_output_folder(work_dir)
    return FileResponse(zip_path, filename=zip_path.name, media_type="application/zip")
