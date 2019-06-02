import xarray as xr
from affine import Affine

dir = '/Users/tommylees/Downloads/dem.tif'
da = xr.open_rasterio(dir)
transform = Affine.from_gdal(*da.attrs['transform'])
