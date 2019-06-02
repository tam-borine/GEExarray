import ee
from geexarray.api import GEEXarray

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

gx.to_xarray(modis_collection, bounds)
