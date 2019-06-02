import ee
# import ee.mapclient
from GEExarray.lib.make_bounds import get_kenya, region_to_polygon

region = get_kenya()
bounds = region_to_polygon(region)
"""
[[33.501, -5.202],
   [42.283, -5.202],
   [42.283, 6.002],
   [33.501, 6.002],
   [33.501, -5.202]]
"""

landsat_collection = (
    ee.ImageCollection('LANDSAT/LE07/C01/T1')
    .filterDate('2000-06-01', '2000-06-11')
    .filterBounds(bounds)
)

modis_collection = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2016-1-31','2016-8-4')
    .filterBounds(bounds)
)


# listOfImages = modis_collection.toList(modis_collection.size());
# image_first = ee.Image(listOfImages.get(0))

#
img = modis_collection.first()
img = img.clip(bounds)

export_region = polygon.getInfo()['coordinates']

task = ee.batch.Export.image.to(
    img,
    description='TEST_TIF',
    fileNamePrefix='TEST_TIF',
    region=export_region,
    scale=30,
)
task.start()
task_id = task.id
print(task_id)
task.status()
