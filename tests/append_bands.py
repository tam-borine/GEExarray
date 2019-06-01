def appendBand_temperature(current, previous):
	"""
	Transforms an Image Collection with 1 band per Image into a single Image with items as bands.
	Makes exporting from Google Earth Engine MUCH simpler/faster!
	(rather than 7 images for 7 bands @each timestep,
	  creates ONE image of ALL BANDS and ALL TIMESTEPS)

	Author: Jamie Vleeshouwer

	Usage:
	-----
	`img_ = imgcoll.iterate(appendBand_modis)`
	"""
	band_list = [0,4]

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
