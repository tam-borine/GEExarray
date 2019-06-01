import ee
import export_tfrecord_to_GCS as GEExarray

ee.Initialize()

ETHIOPIA_POLYGON = [[37.93497660463652,8.022690923975954],
                    [39.27530863588652,7.979173384831735],
                    [39.53898051088652,8.261953466694475],
                    [37.97892191713652,8.39239945580339],
                    [37.93497660463652,8.022690923975954]]

ethiopia_polygon = ee.Geometry.Polygon(ETHIOPIA_POLYGON)


def appendBand_modis(current, previous):
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


modisdata = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2002-12-31','2016-8-4')
    .filterBounds(ethiopia_polygon)
)

GEExarray.export_to_tfrecord(modisdata, ethiopia_polygon)


img_ = modisdata.iterate(appendBand_modis)
image = ee.Image(img_)


name = 'image1'
folder = '_modis'
scale = 500
crs = 'EPSG:4326'

task = ee.batch.Export.image(modisdata, name, {
	'driveFolder': folder,
	'driveFileNamePrefix': name,
	'scale': scale,
	'crs': crs,
})
task.start()

# to produce this as an example!
time = pd.date_range('2002-12-31','2016-8-4',freq='8D')
lon = np.linspace(31.556242254944436, 49.178312567444436, 100)
lat = np.linspace(3.1516405655312387, 15.527940133202428, 100)
band1 = np.random.randint(0, 10, size=(len(time), len(lat), len(lon)))
band2 = np.random.randint(0, 10, size=(len(time), len(lat), len(lon)))
band3 = np.random.randint(0, 10, size=(len(time), len(lat), len(lon)))

eg_ds = xr.Dataset(
    {'band1': (['time', 'lon', 'lat'], band1),
     'band2': (['time', 'lon', 'lat'], band2),
     'band3': (['time', 'lon', 'lat'], band3)},
    coords={
        'time': time,
        'lon': lon,
        'lat': lat,}
)
