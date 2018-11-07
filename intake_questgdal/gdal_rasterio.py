import json
from .base import quest_gdal_base
# from . import __version__


class GDALSource_rasterio(quest_gdal_base):
    """Reads an XY HDF5 table into a dictionary

    Parameters
    ----------
    path: str
        File to load.
    tablename: str
        Name of table to load.
    metadata:
        Arbitrary information to associate with this source.

    """
    name = 'quest_gdal_rasterio'
    container = 'rasterio'
    # version = __version__
    version = '0.0.1'
    partition_access = False

    def __init__(self, path, tablename='dataframe', metadata=None):
        # store important kwargs
        self.path = path
        self.tablename = tablename
        super(GDALSource_rasterio, self).__init__(metadata=metadata)

    def _get_partition(self, _):
        return self.raster_data(self.path)

    def _close(self):
        pass
