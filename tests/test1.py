import ee

ee.Initialize()


ETHIOPIA_POLYGON = [[33.226164129944436, 3.1516405655312387],
                    [49.222257879944436, 3.0638792066536986],
                    [49.178312567444436, 15.527940133202428],
                    [31.556242254944436, 14.849380988829536],
                    [33.226164129944436, 3.1516405655312387]]

ethiopia_polygon = ee.Geometry.Polygon(ETHIOPIA_POLYGON)

# s1data = ee.ImageCollection('COPERNICUS/S1_GRD')

modisdata = (
    ee.ImageCollection('MODIS/006/MOD09A1')
    .filterDate('2002-12-31','2016-8-4')
)

#
