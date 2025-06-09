import asyncio
import io
from pathlib import Path

from fastapi.datastructures import UploadFile
from imxInsights.file.singleFileImx.imxSituationEnum import ImxSituationEnum

from imxInsightsApps.api.main import create_diff, create_population


def make_upload_file(file_path: Path) -> UploadFile:
    file_bytes = file_path.read_bytes()
    file_stream = io.BytesIO(file_bytes)
    return UploadFile(filename=file_path.name, file=file_stream)


def get_file_response_content(response) -> bytes:
    return Path(response.path).read_bytes()


def post_diff(t1_path: Path, t2_path: Path, data: dict) -> tuple[bytes, str]:
    def make_upload_file(path: Path) -> UploadFile:
        return UploadFile(filename=path.name, file=io.BytesIO(path.read_bytes()))

    async def call():
        t1_file = make_upload_file(t1_path)
        t2_file = make_upload_file(t2_path)

        try:
            if not data.get("t1_situation") or not data.get("t2_situation"):
                raise ValueError(
                    "Both 't1_situation' and 't2_situation' must be provided."
                )

            t1_situation = ImxSituationEnum(data["t1_situation"])
            t2_situation = ImxSituationEnum(data["t2_situation"])

            response = await create_diff(
                t1_file=t1_file,
                t2_file=t2_file,
                t1_situation=t1_situation,
                t2_situation=t2_situation,
                geojson=data.get("geojson") == "true",
                to_wgs=data.get("to_wgs") == "true",
                compare_versions=data.get("compare_versions") == "true",
            )
            content = Path(response.path).read_bytes()
            filename = (
                response.headers.get("content-disposition", "")
                .split("filename=")[-1]
                .strip('"')
            )
            return content, filename
        finally:
            await t1_file.close()
            await t2_file.close()

    return asyncio.run(call())


def post_population(imx_path: Path, data: dict) -> tuple[bytes, str]:
    async def inner():
        imx_file = make_upload_file(imx_path)

        try:
            if not data.get("situation"):
                raise ValueError("'situation' must be provided.")

            situation = ImxSituationEnum(data["situation"])

            response = await create_population(
                imx_file=imx_file,
                situation=situation,
                geojson=data.get("geojson") == "true",
                to_wgs=data.get("to_wgs") == "true",
            )
            content = get_file_response_content(response)
            filename = (
                response.headers.get("content-disposition", "")
                .split("filename=")[-1]
                .strip('"')
            )
            return content, filename
        finally:
            await imx_file.close()

    return asyncio.run(inner())
