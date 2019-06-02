import ee
import xarray as xr
import pandas as pd
from IPython.display import Image

import ee.mapclient

# from GEExarray.api import GEEXarray
from GEExarray.lib.make_bounds import get_kenya, region_to_polygon

ee.Initialize()
gx = GEEXarray(bucket_name='geexarray')

polygon = region_to_polygon(get_kenya())

landsat_collection = (
    ee.ImageCollection('LANDSAT/LE07/C01/T1')
    .filterDate('2018-06-01', '2018-06-11')
    .filterBounds(polygon)
)

modis_collection = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2015-12-31','2016-8-4')
    .filterBounds(polygon)
)

image = modis_collection.first()

# ee.mapclient
# gx.to_xarray(modis_collection, polygon)

export_region = polygon.getInfo()['coordinates']

task = ee.batch.Export.image.toDrive(
    image,
    description='TEST_TIF',
    fileNamePrefix='TEST_TIF',
    region=export_region,
    scale=30,
)
task.start()
task_id = task.id
print(task_id)
task.status()
