"""landsat-footprint CLI."""

import os
import json
import click

import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.features import dataset_features
from rio_toa.toa_utils import _get_bounds_from_metadata
from rio_tiler.landsat8 import _landsat_get_mtl, _landsat_parse_scene_id
from shapely.geometry import shape, mapping

from landsat_footprint.utils import landsat_get_ang

LANDSAT_BUCKET = "s3://landsat-pds"


@click.group(short_help="Command line interface")
def l8():
    """landsat-footprint CLI."""
    pass


@l8.command(help="Create footprint from metadata")
@click.argument("sceneid", type=str)
def metadata(sceneid):
    """Create footprint from metadata."""
    geom = {"type": "FeatureCollection", "features": []}

    metadata = _landsat_get_mtl(sceneid)
    m = metadata["L1_METADATA_FILE"]["PRODUCT_METADATA"]
    bbox_geometry = {
        "type": "Feature",
        "properties": {"type": "data bbox"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [m["CORNER_UL_LON_PRODUCT"], m["CORNER_UL_LAT_PRODUCT"]],
                    [m["CORNER_UR_LON_PRODUCT"], m["CORNER_UR_LAT_PRODUCT"]],
                    [m["CORNER_LR_LON_PRODUCT"], m["CORNER_LR_LAT_PRODUCT"]],
                    [m["CORNER_LL_LON_PRODUCT"], m["CORNER_LL_LAT_PRODUCT"]],
                    [m["CORNER_UL_LON_PRODUCT"], m["CORNER_UL_LAT_PRODUCT"]],
                ]
            ],
        },
    }
    geom["features"].append(bbox_geometry)

    nlines = m["REFLECTIVE_LINES"]
    nSamps = m["REFLECTIVE_SAMPLES"]
    bounds = _get_bounds_from_metadata(m)

    ang = landsat_get_ang(sceneid)
    linesBounds = ang["RPC_BAND01"]["BAND01_L1T_IMAGE_CORNER_LINES"]
    sampsBounds = ang["RPC_BAND01"]["BAND01_L1T_IMAGE_CORNER_SAMPS"]

    dlon = bounds[2] - bounds[0]
    dlat = bounds[3] - bounds[1]
    lons = [c / nSamps * dlon + bounds[0] for c in sampsBounds]
    lats = [((nlines - c) / nlines) * dlat + bounds[1] for c in linesBounds]

    data_geometry = {
        "type": "Feature",
        "properties": {"type": "data bounds"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [lons[0], lats[0]],
                    [lons[1], lats[1]],
                    [lons[2], lats[2]],
                    [lons[3], lats[3]],
                    [lons[0], lats[0]],
                ]
            ],
        },
    }
    geom["features"].append(data_geometry)
    click.echo(json.dumps(geom))


@l8.command(help="Create footprint from data")
@click.argument("sceneid", type=str)
@click.option(
    "--band", type=str, default="QA", help="Landsat band to use (default: QA)."
)
@click.option(
    "--overview-level",
    type=int,
    default=1,
    help="Overview level to use. 0: raw data, 4: highest zoom level.",
)
@click.option(
    "--nodata", type=int, default=1, help="Nodata value (default: 1 for QA band)."
)
@click.option("--simplify", is_flag=True, help="Simplify output shape.")
def data(sceneid, band, overview_level, nodata, simplify):
    """Create footprint from data."""
    meta = _landsat_parse_scene_id(sceneid)
    landsat_prefix = os.path.join(LANDSAT_BUCKET, meta["key"])
    s3_path = f"{landsat_prefix}_B{band}.TIF"

    # INFO: we set GDAL_DISABLE_READDIR_ON_OPEN=False to make sure we fetch the ovr
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN=False):
        with rasterio.open(s3_path) as src:
            if overview_level == 0:
                decim = 1
            else:
                decim = src.overviews(1)[overview_level - 1]

            with WarpedVRT(src, nodata=nodata) as vrt:
                feat = list(dataset_features(vrt, bidx=1, sampling=decim, band=False))[
                    0
                ]

                if simplify:
                    g = shape(feat["geometry"])
                    feat["geometry"] = mapping(g.simplify(0.01))

                geom = {"type": "FeatureCollection", "features": [feat]}
                click.echo(json.dumps(geom))
