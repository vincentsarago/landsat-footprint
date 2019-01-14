"""Landsat_footprint utility functions."""

import re
from urllib.request import urlopen

from rio_toa import toa_utils
from rio_tiler.utils import landsat_parse_scene_id


def _parse_ang_txt(angtxt):
    angtxt = angtxt.replace(", \n", ", ")
    group = re.findall(".*\n", angtxt)

    is_group = re.compile(r"GROUP\s\=\s.*")
    is_end = re.compile(r"END_GROUP\s\=\s.*")
    get_group = re.compile(r"=\s([A-Z0-9_\(\)]+)")

    output = [{"key": "all", "data": {}}]

    for g in map(str.lstrip, group):
        if is_group.match(g):
            output.append({"key": get_group.findall(g)[0], "data": {}})

        elif is_end.match(g):
            endk = output.pop()
            k = "{}".format(endk["key"])
            output[-1]["data"][k] = endk["data"]

        else:
            list_group = re.compile(r"^\(.+\)$")
            k, d = toa_utils._parse_data(g)
            if type(d) == str and list_group.match(d):
                d = eval(d.strip())
            if k:
                k = "{}".format(k)
                output[-1]["data"][k] = d

    return output[0]["data"]


def landsat_get_ang(sceneid):
    """Get Landsat-8 MTL metadata

    Attributes
    ----------

    sceneid : str
        Landsat sceneid. For scenes after May 2017,
        sceneid have to be LANDSAT_PRODUCT_ID.

    Returns
    -------
    out : dict
        returns a JSON like object with the metadata.
    """

    scene_params = landsat_parse_scene_id(sceneid)
    s3_key = scene_params["key"]
    meta_file = f"http://landsat-pds.s3.amazonaws.com/{s3_key}_ANG.txt"
    metadata = str(urlopen(meta_file).read().decode())
    return _parse_ang_txt(metadata)
