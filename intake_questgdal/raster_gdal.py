from .base import quest_gdal_base
import xarray as xr
import numpy as np
from .base import Schema
# from . import __version__


class GDALSource(quest_gdal_base):
    """Reads an XY HDF5 table into a dataframe

    Parameters
    ----------
    path: str
        File to load.
    fmt: str
        The requested format to return
    with_nodata: bool
        If true, changes the NODATA value to numpy.nan
    isel_band:
    metadata:
        Arbitrary information to associate with this source.

    """
    name = 'quest_raster_gdal'
    container = 'xarray'
    # version = __version__
    version = '0.0.1'
    partition_access = False

    def __init__(self, path, fmt, with_nodata=False, isel_band=None, metadata=None):
        # store important kwargs
        self.path = path
        self.fmt = fmt

        # Set up the container and name based on the format
        if self.fmt is None or self.fmt.lower() == 'xarray':
            self.container = 'xarray'
        elif self.fmt.lower() == 'rasterio':
            self.container = 'DatasetReader'
        elif self.fmt.lower() == 'array':
            self.container = 'array'
        else:
            raise NotImplementedError('format %s not recognized' % self.fmt)

        self.with_nodata = with_nodata
        self.isel_band = isel_band
        super(GDALSource, self).__init__(metadata=metadata)

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
                if att == 'nodatavals' and self.with_nodata is True:
                    metadata[att] = np.nan
        return Schema(
            datashape=None,
            dtype=str(xarr.dtype),
            shape=xarr.shape,
            npartitions=1,
            extra_metadata=metadata
        )

    def _get_partition(self, _):
        if self.fmt is None or self.fmt.lower() == 'xarray':
            xarr = xr.open_rasterio(self.path, parse_coordinates=True)
            if self.isel_band is not None:
                xarr = xarr.isel(band=0)
            if self.with_nodata:
                xarr = self.convert_nodata_to_nans(xarr)
            return xarr
        elif self.fmt.lower() == 'rasterio':
            return self.raster_data(self.path)
        elif self.fmt.lower() == 'array':
            return self.raster_data(self.path).read()
        else:
            raise NotImplementedError('format %s not recognized' % self.fmt)

    def _close(self):
        pass
