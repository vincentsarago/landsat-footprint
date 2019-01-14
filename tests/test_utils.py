"""tests utils"""

import os

from mock import patch

from landsat_footprint import utils

LANDSAT_SCENE_C1 = "LC08_L1GT_020036_20190103_20190103_01_RT"
LANDSAT_BUCKET = os.path.join(os.path.dirname(__file__), "fixtures", "landsat-pds")

LANDSAT_PATH = os.path.join(
    LANDSAT_BUCKET, "c1", "L8", "020", "036", LANDSAT_SCENE_C1, LANDSAT_SCENE_C1
)


with open("{}_ANG.txt".format(LANDSAT_PATH), "r") as f:
    LANDSAT_ANG_METADATA = f.read()
    LANDSAT_ANG_METADATA_RAW = LANDSAT_ANG_METADATA.encode("utf-8")


def test_parse_ang_txt_valid():
    """Should work as expected (parse _ang data)"""
    meta = utils._parse_ang_txt(LANDSAT_ANG_METADATA)
    assert meta["RPC_BAND01"]["BAND01_L1T_IMAGE_CORNER_LINES"] == (
        4.64299,
        1365.459633,
        7765.634317,
        6374.272081,
    )


@patch("landsat_footprint.utils.urlopen")
def test_landsat_get_mtl_valid(urlopen):
    """Should work as expected (parse sceneid and get _ang metadata)"""
    urlopen.return_value.read.return_value = LANDSAT_ANG_METADATA_RAW
    meta = utils.landsat_get_ang(LANDSAT_SCENE_C1)
    assert meta["RPC_BAND01"]["BAND01_L1T_IMAGE_CORNER_LINES"] == (
        4.64299,
        1365.459633,
        7765.634317,
        6374.272081,
    )
