import dataclasses
import os
import os.path
from typing import List

import pandas as pd
import pytest

from hipscat.catalog import PartitionInfo
from hipscat.catalog.association_catalog.association_catalog_info import AssociationCatalogInfo
from hipscat.catalog.association_catalog.partition_join_info import PartitionJoinInfo
from hipscat.catalog.catalog_info import CatalogInfo
from hipscat.catalog.dataset.base_catalog_info import BaseCatalogInfo
from hipscat.inspection.almanac import Almanac
from hipscat.pixel_math import HealpixPixel

DATA_DIR_NAME = "data"
ALMANAC_DIR_NAME = "almanac"
SMALL_SKY_DIR_NAME = "small_sky"
SMALL_SKY_ORDER1_DIR_NAME = "small_sky_order1"
SMALL_SKY_TO_SMALL_SKY_ORDER1_DIR_NAME = "small_sky_to_small_sky_order1"
TEST_DIR = os.path.dirname(__file__)

# pylint: disable=missing-function-docstring, redefined-outer-name


def pytest_addoption(parser):
    parser.addoption("--cloud", action="store", default="abfs")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.cloud
    if "cloud" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("cloud", [option_value])


@pytest.fixture
def example_cloud_path(cloud):
    if cloud == "abfs":
        return "abfs:///hipscat/pytests/hipscat"

    else:
        raise NotImplementedError("Cloud format not implemented for hipscat tests!")


@pytest.fixture
def example_cloud_storage_options(cloud):
    if cloud == "abfs":
        storage_options = {
            "account_key": os.environ.get("ABFS_LINCCDATA_ACCOUNT_KEY"),
            "account_name": os.environ.get("ABFS_LINCCDATA_ACCOUNT_NAME"),
        }
        return storage_options

    return {}


@pytest.fixture
def tmp_dir_cloud(example_cloud_path):
    return os.path.join(example_cloud_path, "tmp")


@pytest.fixture
def test_data_dir_cloud(example_cloud_path):
    return os.path.join(example_cloud_path, DATA_DIR_NAME)


@pytest.fixture
def almanac_dir_cloud(test_data_dir_cloud):
    return os.path.join(test_data_dir_cloud, ALMANAC_DIR_NAME)


@pytest.fixture
def small_sky_dir_cloud(test_data_dir_cloud):
    return os.path.join(test_data_dir_cloud, SMALL_SKY_DIR_NAME)


@pytest.fixture
def small_sky_order1_dir_cloud(test_data_dir_cloud):
    return os.path.join(test_data_dir_cloud, SMALL_SKY_ORDER1_DIR_NAME)


@pytest.fixture
def small_sky_to_small_sky_order1_dir_cloud(test_data_dir_cloud):
    return os.path.join(test_data_dir_cloud, SMALL_SKY_TO_SMALL_SKY_ORDER1_DIR_NAME)


@pytest.fixture
def catalog_pixels() -> List[HealpixPixel]:
    return [HealpixPixel(1, 0), HealpixPixel(1, 1), HealpixPixel(2, 8)]


@pytest.fixture
def association_catalog_path_cloud(test_data_dir_cloud) -> str:
    return os.path.join(test_data_dir_cloud, "small_sky_to_small_sky_order1")


@pytest.fixture
def association_catalog_info_file_cloud(association_catalog_path_cloud) -> str:
    return os.path.join(association_catalog_path_cloud, "catalog_info.json")


@pytest.fixture
def index_catalog_info_file_cloud(test_data_dir_cloud) -> str:
    return os.path.join(test_data_dir_cloud, "index_catalog", "catalog_info.json")


@pytest.fixture
def margin_cache_catalog_info_file_cloud(test_data_dir_cloud) -> str:
    return os.path.join(test_data_dir_cloud, "margin_cache", "catalog_info.json")


@pytest.fixture
def source_catalog_info_file_cloud(test_data_dir_cloud) -> str:
    return os.path.join(test_data_dir_cloud, "small_sky_source", "catalog_info.json")


@pytest.fixture
def association_catalog_info(association_catalog_info_data) -> AssociationCatalogInfo:
    return AssociationCatalogInfo(**association_catalog_info_data)


@pytest.fixture
def association_catalog_partition_join_file_cloud(association_catalog_path_cloud) -> str:
    return os.path.join(association_catalog_path_cloud, "partition_join_info.csv")


@pytest.fixture
def dataset_path_cloud(test_data_dir_cloud) -> str:
    return os.path.join(test_data_dir_cloud, "dataset")


@pytest.fixture
def base_catalog_info_file_cloud(dataset_path_cloud) -> str:
    return os.path.join(dataset_path_cloud, "catalog_info.json")


@pytest.fixture
def base_catalog_info(base_catalog_info_data) -> BaseCatalogInfo:
    return BaseCatalogInfo(**base_catalog_info_data)


@pytest.fixture
def catalog_path_cloud(test_data_dir_cloud) -> str:
    return os.path.join(test_data_dir_cloud, "catalog")


@pytest.fixture
def catalog_info_file_cloud(catalog_path_cloud) -> str:
    return os.path.join(catalog_path_cloud, "catalog_info.json")


@pytest.fixture
def test_data_dir():
    return os.path.join(TEST_DIR, DATA_DIR_NAME)


@pytest.fixture
def small_sky_dir_local(test_data_dir):
    return os.path.join(test_data_dir, SMALL_SKY_DIR_NAME)


@pytest.fixture
def small_sky_order1_dir_local(test_data_dir):
    return os.path.join(test_data_dir, SMALL_SKY_ORDER1_DIR_NAME)


@pytest.fixture
def assert_catalog_info_matches_dict():
    def assert_match(catalog_info: BaseCatalogInfo, dictionary: dict):
        """Check that all members of the catalog_info object match dictionary
        elements, where specified."""
        catalog_info_dict = dataclasses.asdict(catalog_info)
        for key, value in dictionary.items():
            assert catalog_info_dict[key] == value

    return assert_match


@pytest.fixture
def base_catalog_info_data() -> dict:
    return {
        "catalog_name": "test_name",
        "catalog_type": "object",
        "total_rows": 10,
    }


@pytest.fixture
def catalog_info_data() -> dict:
    return {
        "catalog_name": "test_name",
        "catalog_type": "object",
        "total_rows": 10,
        "epoch": "J2000",
        "ra_column": "ra",
        "dec_column": "dec",
    }


@pytest.fixture
def association_catalog_info_data() -> dict:
    return {
        "catalog_name": "test_name",
        "catalog_type": "association",
        "total_rows": 10,
        "primary_catalog": "small_sky",
        "primary_column": "id",
        "join_catalog": "small_sky_order1",
        "join_column": "id",
    }


@pytest.fixture
def source_catalog_info() -> dict:
    return {
        "catalog_name": "test_source",
        "catalog_type": "source",
        "total_rows": 100,
        "epoch": "J2000",
        "ra_column": "source_ra",
        "dec_column": "source_dec",
    }


@pytest.fixture
def source_catalog_info_with_extra() -> dict:
    return {
        "catalog_name": "test_source",
        "catalog_type": "source",
        "total_rows": 100,
        "epoch": "J2000",
        "ra_column": "source_ra",
        "dec_column": "source_dec",
        "primary_catalog": "test_name",
        "mjd_column": "mjd",
        "band_column": "band",
        "mag_column": "mag",
        "mag_err_column": "",
    }


@pytest.fixture
def margin_cache_catalog_info() -> dict:
    return {
        "catalog_name": "test_margin",
        "catalog_type": "margin",
        "total_rows": 100,
        "primary_catalog": "test_name",
        "margin_threshold": 0.5,
    }


@pytest.fixture
def index_catalog_info() -> dict:
    return {
        "catalog_name": "test_index",
        "catalog_type": "index",
        "total_rows": 100,
        "primary_catalog": "test_name",
        "indexing_column": "id",
    }


@pytest.fixture
def index_catalog_info_with_extra() -> dict:
    return {
        "catalog_name": "test_index",
        "catalog_type": "index",
        "total_rows": 100,
        "primary_catalog": "test_name",
        "indexing_column": "id",
        "extra_columns": ["foo", "bar"],
    }


@pytest.fixture
def catalog_info(catalog_info_data) -> CatalogInfo:
    return CatalogInfo(**catalog_info_data)


@pytest.fixture
def association_catalog_join_pixels() -> pd.DataFrame:
    return pd.DataFrame.from_dict(
        {
            PartitionJoinInfo.PRIMARY_ORDER_COLUMN_NAME: [0, 0, 0, 0],
            PartitionJoinInfo.PRIMARY_PIXEL_COLUMN_NAME: [11, 11, 11, 11],
            PartitionJoinInfo.JOIN_ORDER_COLUMN_NAME: [1, 1, 1, 1],
            PartitionJoinInfo.JOIN_PIXEL_COLUMN_NAME: [44, 45, 46, 47],
        }
    )


@pytest.fixture
def default_almanac_cloud(example_cloud_path, example_cloud_storage_options):
    """Set up default environment variables and fetch default almanac data."""

    test_data_dir = os.path.join(example_cloud_path, "data")
    almanac_dir = os.path.join(example_cloud_path, "data", "almanac")

    os.environ["HIPSCAT_ALMANAC_DIR"] = almanac_dir
    os.environ["HIPSCAT_DEFAULT_DIR"] = test_data_dir

    return Almanac(storage_options=example_cloud_storage_options)
