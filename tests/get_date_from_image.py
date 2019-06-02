import ee
from GEExarray.lib.make_bounds import get_kenya, region_to_polygon

polygon = region_to_polygon(get_kenya())
bounds = polygon.bounds()

landsat_collection = (
    ee.ImageCollection('LANDSAT/LE07/C01/T1')
    .filterDate('2018-06-01', '2018-06-11')
    .filterBounds(bounds)
)

modis_collection = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2015-12-31','2016-8-4')
    .filterBounds(bounds)
)

image = landsat_collection.first()
date = ee.Date(collection.first().get('system:time_start'))
date_dict = date.format('Y-MM-dd').getInfo()
