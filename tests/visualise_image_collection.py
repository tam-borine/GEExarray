import ee
import ee.mapclient
from GEExarray.lib.make_bounds import get_kenya, region_to_polygon
# ee.mapclient.centerMap(-122.45, 37.75, 13)

region = get_kenya()
bounds = region_to_polygon(region)

landsat_collection = (
    ee.ImageCollection('LANDSAT/LE07/C01/T1')
    .filterDate('2000-06-01', '2000-06-11')
    .filterBounds(bounds)
)

modis_collection = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2002-12-31','2016-8-4')
    .filterBounds(bounds)
)

image = modis_collection.first()

ee.mapclient.addToMap(image)
