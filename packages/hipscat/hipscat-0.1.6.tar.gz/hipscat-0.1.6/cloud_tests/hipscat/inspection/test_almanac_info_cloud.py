import dataclasses
import os

import pytest

from hipscat.inspection.almanac import Almanac
from hipscat.inspection.almanac_info import AlmanacInfo
from hipscat.io.file_io import file_io


def test_from_catalog_dir(small_sky_dir_cloud, example_cloud_storage_options):
    """Load from a directory."""
    almanac_info = AlmanacInfo.from_catalog_dir(
        small_sky_dir_cloud, storage_options=example_cloud_storage_options
    )
    assert almanac_info.catalog_name == "small_sky"


def test_from_bad_file(association_catalog_partition_join_file_cloud, example_cloud_storage_options):
    """Test failures when loading almanac from invalid files."""
    with pytest.raises(ValueError, match="csv"):
        AlmanacInfo.from_file(
            association_catalog_partition_join_file_cloud, storage_options=example_cloud_storage_options
        )


def test_write_to_file(tmp_dir_cloud, association_catalog_path_cloud, example_cloud_storage_options):
    """Write out the almanac to file and make sure we can read it again."""
    almanac_info = AlmanacInfo.from_catalog_dir(
        association_catalog_path_cloud, storage_options=example_cloud_storage_options
    )
    assert almanac_info.catalog_name == "small_sky_to_small_sky_order1"
    almanac_info.version = "v0.0.1"
    almanac_info.deprecated = "yes - use something else"
    almanac_info.creators.append("me")

    almanac_info.write_to_file(
        tmp_dir_cloud, default_dir=False, storage_options=example_cloud_storage_options
    )

    new_info = AlmanacInfo.from_file(
        os.path.join(tmp_dir_cloud, "small_sky_to_small_sky_order1.yml"),
        storage_options=example_cloud_storage_options,
    )

    assert new_info.catalog_name == almanac_info.catalog_name

    almanac_info_dict = dataclasses.asdict(almanac_info)
    new_info_dict = dataclasses.asdict(new_info)
    for key, value in new_info_dict.items():
        assert almanac_info_dict[key] == value

    file_io.delete_file(
        os.path.join(tmp_dir_cloud, "small_sky_to_small_sky_order1.yml"),
        storage_options=example_cloud_storage_options,
    )


def test_write_to_file_load_almanac(tmp_dir_cloud, small_sky_dir_cloud, example_cloud_storage_options):
    """Write out the almanac to file and make sure we can read it again."""
    almanac_info = AlmanacInfo.from_catalog_dir(
        small_sky_dir_cloud, storage_options=example_cloud_storage_options
    )
    assert almanac_info.catalog_name == "small_sky"

    almanac_info.write_to_file(
        tmp_dir_cloud, default_dir=False, storage_options=example_cloud_storage_options
    )

    alms = Almanac(
        include_default_dir=False, dirs=tmp_dir_cloud, storage_options=example_cloud_storage_options
    )
    assert len(alms.catalogs()) == 1

    file_io.delete_file(
        os.path.join(tmp_dir_cloud, "small_sky.yml"), storage_options=example_cloud_storage_options
    )


def test_write_to_bad_file(tmp_dir_cloud, small_sky_dir_cloud, example_cloud_storage_options):
    """Test failure conditions when writing almanac."""
    os.environ["HIPSCAT_ALMANAC_DIR"] = str(tmp_dir_cloud)
    almanac_info = AlmanacInfo.from_catalog_dir(
        small_sky_dir_cloud, storage_options=example_cloud_storage_options
    )

    with pytest.raises(ValueError, match="only one"):
        almanac_info.write_to_file(
            tmp_dir_cloud, default_dir=True, storage_options=example_cloud_storage_options
        )

    with pytest.raises(ValueError, match="foo"):
        almanac_info.write_to_file(fmt="foo", storage_options=example_cloud_storage_options)

    almanac_info.write_to_file(default_dir=True, storage_options=example_cloud_storage_options)
    with pytest.raises(ValueError, match="already exists"):
        almanac_info.write_to_file(default_dir=True, storage_options=example_cloud_storage_options)

    file_io.delete_file(
        os.path.join(tmp_dir_cloud, "small_sky.yml"), storage_options=example_cloud_storage_options
    )


def test_association_fields(
    association_catalog_path_cloud,
    index_catalog_info_file_cloud,
    small_sky_dir_cloud,
    example_cloud_storage_options,
):
    """Test additional text fields tables with primary/join relationships."""
    almanac_info = AlmanacInfo.from_catalog_dir(
        association_catalog_path_cloud, storage_options=example_cloud_storage_options
    )
    assert almanac_info.catalog_name == "small_sky_to_small_sky_order1"
    assert almanac_info.primary == "small_sky"
    assert almanac_info.join == "small_sky_order1"

    almanac_info = AlmanacInfo.from_catalog_dir(
        index_catalog_info_file_cloud, storage_options=example_cloud_storage_options
    )
    assert almanac_info.primary == "catalog"
    assert almanac_info.join is None

    almanac_info = AlmanacInfo.from_catalog_dir(
        small_sky_dir_cloud, storage_options=example_cloud_storage_options
    )
    assert almanac_info.primary is None
    assert almanac_info.join is None


## Commented out -
## As new test catalogs are added, you can use this method to quickly add
## their almanac to the default almanac directory
# def test_add_almanac(source_catalog_info_file):
#     """Write out the almanac to file and make sure we can read it again."""
#     almanac_info = AlmanacInfo.from_catalog_dir(source_catalog_info_file)
#     almanac_info.write_to_file()
