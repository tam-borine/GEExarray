import ee, datetime
import pandas as pd
import geopandas as gpd
import matplotlib.dates as mdates
from IPython.display import Image
from matplotlib import dates
from shapely.geometry import shape
import skimage
ee.Initialize()
# %matplotlib inline

# ==========================================================================
# Function to Convert Feature Classes to Pandas Dataframe
# Adapted from: https://events.hpc.grnet.gr/event/47/material/1/12.py
def fc2df(fc):
    # Convert a FeatureCollection into a pandas DataFrame
    # Features is a list of dict with the output
    features = fc.getInfo()['features']

    dictarr = []

    for f in features:
        # Store all attributes in a dict
        attr = f['properties']
        # and treat geometry separately
        attr['geometry'] = f['geometry']  # GeoJSON Feature!
        # attr['geometrytype'] = f['geometry']['type']
        dictarr.append(attr)

    df = gpd.GeoDataFrame(dictarr)
    # Convert GeoJSON features to shape
    df['geometry'] = map(lambda s: shape(s), df.geometry)
    return df

# ==========================================================================
# Function to iterate over image collection, returning a pandas dataframe
def extract_point_values(img_id, pts):
    image = ee.Image(img_id)

    fc_image_red = image.reduceRegions(collection=pts,
                                  reducer=ee.Reducer.mean(),
                                  scale=30)

    # Convert to Pandas Dataframe
    df_image_red = fc2df(fc_image_red)

    # Add Date as Variable
    df_image_red['date'] = image.getInfo()['properties']['DATE_ACQUIRED']

    return df_image_red

# ==========================================================================
#### Make Points
points = ee.FeatureCollection([
            ee.Feature(ee.Geometry.Point(14.742607, -17.494993)),
            ee.Feature(ee.Geometry.Point(14.715903, -17.450650)),
            ])

#### Load Raster
l8 = ee.ImageCollection('LANDSAT/LC8_L1T').filterDate('2015-01-01', '2015-12-31').filterBounds(points)

#### Make list of image IDs
l8_id = []
for f in l8.getInfo()['features']:
  image_id = f['properties']['LANDSAT_SCENE_ID'].encode('ascii', 'ignore')
  image_id = 'LANDSAT/LC8_L1T/' + image_id.decode("utf-8")
  l8_id.append(image_id)

#### Create Initial Pandas Dataframe
df_all = extract_point_values(l8_id[0], points)
df_all = df_all.drop([0,1])

#### Iterate over all images
for i in l8_id:
    df_all = df_all.append(extract_point_values(i, points))

#### Display Results
df_all
