# GEExarray
Export GEE Collections to xarray

# Aims
- Be able to export `ee.ImageCollection` to python `xarray.Dataset` objects with labelled `lat`,`lon`,`time` coordinates

```
<xarray.Dataset>
Dimensions:  (lat: 45, lon: 35, time: 1430)
Coordinates:
  * time     (time) datetime64[ns] 1900-01-01 1900-02-01 ... 2019-02-01
  * lon      (lon) float32 33.625 33.875 34.125 34.375 ... 41.625 41.875 42.125
  * lat      (lat) float32 -5.125 -4.875 -4.625 -4.375 ... 5.375 5.625 5.875
Data variables:
    precip   (time, lat, lon) float32 ...
```

# Install

(Coming soon):
`pip install geexarray`

# Set up Google Cloud Storage (GCS)

As currently GEE exports only to Google Drive and Google Cloud Storage, we will need to use the latter as an intermediary for now. Ensure you have an account with [GCS](https://cloud.google.com/storage/) and create a project and buckets for your data.

# Using GEEXarray

For each ImageCollection you want to convert to an xarray dataset, make a new instance of GEEXarray, specifying your GCS bucket name and credentials file like so:

```
from geexarray.api import GEEXarray

gx = GEEXarray('the_best_bucket')

gx.to_xarray(my_imagecollection, geometry_bounds_object)
```

The optional timeout parameter specifies how long you are happy to wait for the export from GEE. This will vary by the size of the ImageCollection you are exporting. Defaults to 10 minutes. You can reduce it by decreasing the size of geometry bounds, or [filtering](https://developers.google.com/earth-engine/ic_filtering) your ImageCollection to a narrower date range.

## References
- [Discussion on `Pangeo` github thread](https://github.com/pangeo-data/pangeo/issues/216)
- [Writing netCDF files to GEE](http://arbennett.github.io/software,/hydrology/2017/07/30/netcdfToGEE.html)
- [Iterating over ImageCollection and Downloading](https://stackoverflow.com/a/46961005/9940782)
- [Extracting images that meet a criteria from EE](https://gis.stackexchange.com/questions/315541/extracting-qualified-image-patches-in-google-earth-engine)
- [Processing Rainfall data from EE](https://gis.stackexchange.com/questions/293076/python-script-tool-fails-when-processing-rainfall-data-from-google-earth-engine)
- [ImageCollection to DataFrame](https://gis.stackexchange.com/questions/257727/iterate-over-imagecollection-returning-pandas-dataframe-using-earth-engine-pyt?rq=1)
- [to DF](https://gis.stackexchange.com/a/257748/123489)
- [Clipping vs. Filtering](https://gis.stackexchange.com/questions/247955/clipping-vs-filtering-images-with-a-polygon-google-earth-engine)

## The major functions
1. Append lat lon to imageCollection
    ```
    collection = collection.map(
        lambda im: im.addBands(ee.Image.pixelLonLat())
    )
    ```

2. Append time to imageCollection
    ```

    ```
