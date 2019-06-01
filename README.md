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

## References
- [Discussion on `Pangeo` github thread](https://github.com/pangeo-data/pangeo/issues/216)
- [Writing netCDF files to GEE](http://arbennett.github.io/software,/hydrology/2017/07/30/netcdfToGEE.html)
