from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# from .raster_gdal_xarray import GDALSource_xarray
# from .raster_gdal_rasterio import GDALSource_rasterio
# from .raster_gdal_array import GDALSource_array
from .raster_gdal import GDALSource
