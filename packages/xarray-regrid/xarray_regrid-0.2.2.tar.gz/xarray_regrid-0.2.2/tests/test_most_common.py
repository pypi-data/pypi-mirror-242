import numpy as np
import pytest
import xarray as xr

from xarray_regrid import Grid, create_regridding_dataset


@pytest.fixture
def dummy_lc_data():
    data = np.array(
        [
            [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [3, 3, 3, 3, 0, 0, 0, 0, 1, 1, 1],
            [3, 3, 0, 3, 0, 0, 0, 0, 1, 1, 1],
        ]
    )
    lat_coords = np.linspace(0, 40, num=11)
    lon_coords = np.linspace(0, 40, num=11)

    return xr.Dataset(
        data_vars={
            "lc": (["longitude", "latitude"], data),
        },
        coords={
            "longitude": (["longitude"], lon_coords),
            "latitude": (["latitude"], lat_coords),
        },
    )


@pytest.fixture
def dummy_target_grid():
    new_grid = Grid(
        north=40,
        east=40,
        south=0,
        west=0,
        resolution_lat=8,
        resolution_lon=8,
    )
    return create_regridding_dataset(new_grid)


def test_most_common(dummy_lc_data, dummy_target_grid):
    expected_data = np.array(
        [
            [2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [3, 3, 0, 0, 0, 1],
        ]
    )

    lat_coords = np.linspace(0, 40, num=6)
    lon_coords = np.linspace(0, 40, num=6)

    expected = xr.Dataset(
        data_vars={
            "lc": (["longitude", "latitude"], expected_data),
        },
        coords={
            "longitude": (["longitude"], lon_coords),
            "latitude": (["latitude"], lat_coords),
        },
    )
    xr.testing.assert_equal(
        dummy_lc_data.regrid.most_common(dummy_target_grid)["lc"],
        expected["lc"],
    )
