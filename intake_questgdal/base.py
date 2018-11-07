from intake.source.base import DataSource, Schema
import rasterio
import xarray as xr
import warnings
# from . import __version__

class quest_gdal_base(DataSource):
    """Reads an HDF5 table

    Parameters
    ----------
    path: str
        File to load.
    tablename: str
        Name of table to load.
    metadata:
        Arbitrary information to associate with this source.

    """
    #version = __version__
    version = '0.0.1'
    container = 'dataframe'
    partition_access = False
    path = ''

    # def _get_schema(self):
    #     self._schema = Schema(
    #         datashape=None,
    #         dtype=None,
    #         shape=None,
    #         npartitions=1,
    #         extra_metadata={}
    #     )
    #     return self._schema

    def _get_schema(self):
        if self.path is not '':
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
        else:
            self._schema = Schema(
                datashape=None,
                dtype=None,
                shape=None,
                npartitions=1,
                extra_metadata={}
            )
            return self._schema

    def _get_partition(self, _):
        return None

    def _close(self):
        pass

    def raster_data(self, path):
        return rasterio.open(path)
