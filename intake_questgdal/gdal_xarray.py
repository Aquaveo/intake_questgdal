from .base import quest_gdal_base
import xarray as xr
import numpy as np
from .base import Schema
# from . import __version__


class GDALSource_xarray(quest_gdal_base):
    """Reads an XY HDF5 table into a dataframe

    Parameters
    ----------
    path: str
        File to load.
    tablename: str
        Name of table to load.
    metadata:
        Arbitrary information to associate with this source.

    """
    name = 'quest_gdal_xarray'
    container = 'xarray'
    #version = __version__
    version = '0.0.1'
    partition_access = False

    def __init__(self, path, tablename='dataframe', metadata=None):
        # store important kwargs
        self.path = path
        self.tablename = tablename
        self.with_nodata = False
        self.isel_band = None
        self._ds = None
        super(GDALSource_xarray, self).__init__(metadata=metadata)

    def convert_nodata_to_nans(self, xarr):
        nodata_attr = [k for k in xarr.attrs.keys() if k.lower().startswith('nodata')][0]
        nodata = xarr.attrs[nodata_attr]
        if nodata:
            if str(xarr.dtype).startswith('int') or str(xarr.dtype).startswith('uint'):
                xarr.values = xarr.values.astype(np.float32)
            xarr.values[xarr.values == nodata] = np.nan
        return xarr

    def _get_schema(self):
        xarr = xr.open_rasterio(self.path)
        ds2 = xr.Dataset({'raster': xarr})
        metadata = {
            'dims': dict(ds2.dims),
            'data_vars': {k: list(ds2[k].coords)
                          for k in ds2.data_vars.keys()},
            'coords': tuple(ds2.coords.keys()),
            'array': 'raster'
        }
        atts = ['transform', 'crs', 'res', 'is_tiled', 'nodatavals']
        for att in atts:
            if att in xarr.attrs:
                metadata[att] = xarr.attrs[att]
        return Schema(
            datashape=None,
            dtype = str(xarr.dtype),
            shape=xarr.shape,
            npartitions=1,
            extra_metadata=metadata
        )

    def _get_partition(self, _):
        xarr = xr.open_rasterio(self.path, parse_coordinates=True)
        if self.isel_band is not None:
            xarr = xarr.isel(band=0)
        if self.with_nodata:
            xarr = self.convert_nodata_to_nans(xarr)
        return xarr

    def _close(self):
        pass
