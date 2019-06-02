def clip_to_bbox(img, lat, lon, box_size):
	""" """
	# filter to create a 50km*50km square buffer centered on the lat/lon point
	bbox_list = boundingBox(lat, lon, box_size/2)
	bbox = ee.Geometry.Rectangle(bbox_list)
	# clip the modis data to the extent of the 50km bounding box
	clipped_image = img.clip(bbox)

	return clipped_image


def export_ee_image(img, folder_name, index, lat, lon):
	"""
	Helper function to apply the functions to each image.

	a) create unique bounding box around the latlon point
	b) clip the JOINED image to this bounding box
	c) export to google drive
	"""
	fname = f"{folder_name}_{int(index)}"
	box_size = 50 # in km, *1/2
	scale = 500
	crs = 'EPSG:4326'

    clipped_image = clip_to_bbox(img, lat, lon, box_size)
