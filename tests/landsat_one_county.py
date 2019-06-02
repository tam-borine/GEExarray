import ee
import sys
import os

if os.getcwd().split('/')[-2] == 'GEExarray':
    sys.path.append('..')

print(os.getcwd())
print(sys.path)

from GEExarray.api import GEEXarray

gx = GEEXarray()

ee.Initialize()

table = ee.FeatureCollection("TIGER/2016/Counties");
county = table.filterMetadata('NAMELSAD','equals','Bracken County');
bounds = ee.Feature(county);

landsat_collection = (
    ee.ImageCollection('LANDSAT/LE07/C01/T1')
    .filterDate('2000-06-01', '2000-06-11')
)

modis_collection = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2002-12-31','2016-8-4')
)

gx.to_xarray(landsat_collection, bounds)
