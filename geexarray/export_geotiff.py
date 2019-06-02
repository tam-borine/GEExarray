import ee
from ee import batch

import fiona

from GEExarray.lib.make_bounds import get_kenya, region_to_polygon

def read_feature(shapefile):
    """Extract the geometry from the shapefile (for masking the ee.Image object) """
    with fiona.open(shapefile) as src:
        feature_col = src["geometry"]
        return feature_col


def appendBands(current, previous):
	"""
	Transforms an Image Collection with 1 band per Image into a single Image with items as bands.
	Makes exporting from Google Earth Engine MUCH simpler/faster!
	(rather than 7 images for 7 bands @each timestep,
	  creates ONE image of ALL BANDS and ALL TIMESTEPS)

	Author: Jamie Vleeshouwer
	"""
	band_list = [0,1,2,3,4,5,6]

	# Rename the band
	previous = ee.Image(previous)
	current = current.select(band_list)
	# Append it to the result (Note: only return current item on first element/iteration)
	accum = ee.Algorithms.If(
		ee.Algorithms.IsEqual(previous, None),
		current,
		previous.addBands(ee.Image(current))
		)
	# Return the accumulation
	return accum




def get_sentinel(
    product: str, aoi,
    start_date: str, end_date: str,
    bands=["B2", "B3", "B4", "B8"],
    export=False,):

    kenya_region = region_to_polygon(get_kenya())
    col = (
        ee.ImageCollection(product)
        .filterBounds(kenya_region.getInfo()['coordinates'])
        .filterDate(start_date, end_date)
        .map(sentinel_cloud_mask)
    )
    mosaic = ee.ImageCollection([col.select(bands)]).mosaic()

    if export is False:
        return mosaic

    # do the export
    task_config = {
        "description": "imageToDriveExample",
        "scale": 30,
        "crs": "EPSG:4326",
    }
    task = (
        batch.Export.image.toDrive(
            mosaic, "00_exported_image", task_config
        )
    )

    task.start()
