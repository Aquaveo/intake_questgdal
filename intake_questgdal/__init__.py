from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .gdal_xarray import GDALSource_xarray
from .gdal_rasterio import GDALSource_rasterio
from .gdal_array import GDALSource_array
