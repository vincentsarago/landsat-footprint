"""tests cli"""

import os
import json
import pytest

from mock import patch

from click.testing import CliRunner

from rio_toa.toa_utils import _parse_mtl_txt
from landsat_footprint.utils import _parse_ang_txt
from landsat_footprint.scripts import cli
from landsat_footprint.scripts.cli import l8

LANDSAT_SCENE_C1 = "LC08_L1GT_020036_20190103_20190103_01_RT"
LANDSAT_BUCKET = os.path.join(os.path.dirname(__file__), "fixtures", "landsat-pds")

LANDSAT_PATH = os.path.join(
    LANDSAT_BUCKET, "c1", "L8", "020", "036", LANDSAT_SCENE_C1, LANDSAT_SCENE_C1
)


with open("{}_ANG.txt".format(LANDSAT_PATH), "r") as f:
    LANDSAT_ANG_METADATA = _parse_ang_txt(f.read())

with open("{}_MTL.txt".format(LANDSAT_PATH), "r") as f:
    LANDSAT_METADATA = _parse_mtl_txt(f.read())


@pytest.fixture(autouse=True)
def testing_env_var(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "jqt")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "rde")
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    monkeypatch.setenv("AWS_CONFIG_FILE", "/tmp/noconfigheere")
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", "/tmp/noconfighereeither")


def test_l8_valid():
    """Should work as expected."""
    runner = CliRunner()
    result = runner.invoke(l8)
    assert not result.exception
    assert result.exit_code == 0


@patch("landsat_footprint.scripts.cli.landsat_get_mtl")
@patch("landsat_footprint.scripts.cli.landsat_get_ang")
def test_metadata_valid(landsat_get_ang, landsat_get_mtl):
    """Should work as expected."""
    landsat_get_mtl.return_value = LANDSAT_METADATA
    landsat_get_ang.return_value = LANDSAT_ANG_METADATA

    runner = CliRunner()
    result = runner.invoke(l8, ["metadata", LANDSAT_SCENE_C1])
    assert len(json.loads(result.output)["features"]) == 2
    assert not result.exception
    assert result.exit_code == 0


def test_data_valid(monkeypatch):
    """Should work as expected."""
    monkeypatch.setattr(cli, "LANDSAT_BUCKET", LANDSAT_BUCKET)

    runner = CliRunner()
    result = runner.invoke(l8, ["data", LANDSAT_SCENE_C1])
    feats = json.loads(result.output)["features"]
    assert len(feats) == 1
    assert len(feats[0]["geometry"]["coordinates"][0]) == 3681
    assert not result.exception
    assert result.exit_code == 0


def test_data_valid_raw(monkeypatch):
    """Should work as expected."""
    monkeypatch.setattr(cli, "LANDSAT_BUCKET", LANDSAT_BUCKET)

    runner = CliRunner()
    result = runner.invoke(l8, ["data", LANDSAT_SCENE_C1, "--overview-level", "0"])
    feats = json.loads(result.output)["features"]
    assert len(feats) == 1
    assert len(feats[0]["geometry"]["coordinates"][0]) == 11031
    assert not result.exception
    assert result.exit_code == 0


def test_data_valid_simplify(monkeypatch):
    """Should work as expected."""
    monkeypatch.setattr(cli, "LANDSAT_BUCKET", LANDSAT_BUCKET)

    runner = CliRunner()
    result = runner.invoke(l8, ["data", LANDSAT_SCENE_C1, "--simplify"])
    feats = json.loads(result.output)["features"]
    assert len(feats) == 1
    assert len(feats[0]["geometry"]["coordinates"][0]) == 5
    assert not result.exception
    assert result.exit_code == 0
