from fastapi.testclient import TestClient

from imxInsightsApps.api.main import api_app

client = TestClient(api_app)


def post_diff(t1_path, t2_path, data: dict) -> tuple[bytes, str]:
    with open(t1_path, "rb") as t1, open(t2_path, "rb") as t2:
        response = client.post(
            "/diff",
            files={"t1_file": ("t1.xml", t1), "t2_file": ("t2.xml", t2)},
            data=data,
        )
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        content_disp = response.headers.get("content-disposition", "")
        filename = "diff_result.zip"
        if "filename=" in content_disp:
            filename = content_disp.split("filename=")[-1].strip('"')

        return response.content, filename


def post_population(imx_path, data: dict) -> tuple[bytes, str]:
    with open(imx_path, "rb") as imx:
        response = client.post(
            "/population",
            files={"imx_file": ("imx.xml", imx)},
            data=data,
        )
        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        content_disp = response.headers.get("content-disposition", "")
        filename = "population_result.zip"
        if "filename=" in content_disp:
            filename = content_disp.split("filename=")[-1].strip('"')

        return response.content, filename
