import pytest

from tests.helpers import sample_path


@pytest.fixture(scope="module")
def issue_list() -> str:
    return sample_path("issuelist.xlsx")


@pytest.fixture(scope="module")
def imx_12_container_file() -> str:
    return sample_path("imx_12_container.zip")


@pytest.fixture(scope="module")
def imx_single_xml_file() -> str:
    return sample_path("imx_12_container.zip")
