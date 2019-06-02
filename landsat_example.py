import ee
from geexarray.api import GEEXarray

ee.Initialize()
gx = GEEXarray()

UTAH_POLYGON = [
    [-114.53593749999999,39.21923019881908],
    [-109.61406249999999,34.29325621656583],
    [-109.70195312499999,40.634547146777386],
     [-114.53593749999999,39.21923019881908]
    ]

bounds = ee.Geometry.Polygon(UTAH_POLYGON)

landsat_collection = ee.ImageCollection('LANDSAT/LE07/C01/T1').filterDate('2000-06-01', '2000-06-11')
modisdata = ee.ImageCollection('MODIS/006/MOD09A1').filterDate('2002-12-31','2016-8-4')
# a user should just be able to say to_xarray(collection)

gx.to_xarray(modisdata, bounds)

# once it has exported we want to pull convert