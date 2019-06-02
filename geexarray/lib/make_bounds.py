from collections import namedtuple
import ee
from typing import List
Polygon = ee.Geometry.Polygon

Region = namedtuple('Region', ['name', 'lonmin', 'lonmax', 'latmin', 'latmax'])


def get_kenya() -> Region:
    """This pipeline is focused on drought prediction in Kenya.
    This function allows Kenya's bounding box to be easily accessed
    by all exporters.
    """
    return Region(name='kenya', lonmin=33.501, lonmax=42.283,
                  latmin=-5.202, latmax=6.002)


def get_gee_bounds(region: Region) -> List:
    """return bounds to be turned into format readable for """
    bounds = [
        [region.lonmin, region.latmin],
        [region.lonmax, region.latmin],
        [region.lonmax, region.latmax],
        [region.lonmin, region.latmax],
        [region.lonmin, region.latmin],
    ]
    return bounds


def bounds_to_ee_polygon(bounds: List) -> Polygon:
    polygon = ee.Geometry.Polygon(bounds)
    return polygon


def region_to_polygon(region: Region) -> Polygon:
    """Convert a region object into an ee.Polygon
    that can be used to subset our
    """
    bounds = get_gee_bounds(region)
    polygon = bounds_to_ee_polygon(bounds)
    return polygon
