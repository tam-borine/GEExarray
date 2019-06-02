import ee
import sys
import os

from GEExarray.lib.make_bounds import get_kenya, region_to_polygon
from GEExarray.api import GEEXarray

gx = GEEXarray()

ee.Initialize()

# table = ee.FeatureCollection("TIGER/2016/Counties");
# county = table.filterMetadata('NAMELSAD','equals','Bracken County');
# bounds = ee.Feature(county);

region = get_kenya()
bounds = region_to_polygon(region)

landsat_collection = (
    ee.ImageCollection('LANDSAT/LE07/C01/T1')
    .filterDate('2000-06-01', '2000-06-11')
)

modis_collection = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2002-12-31','2016-8-4')
)

print("Exporting MODIS to Cloud")
gx.to_xarray(modis_collection, bounds)

#
