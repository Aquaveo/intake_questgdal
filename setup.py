#!/usr/bin/env python
from setuptools import setup, find_packages
import versioneer

setup(
    name='intake-questgdal',
    version=versioneer.get_version(),
    description='Quest GDAL plugins for Intake',
    url='',
    maintainer='',
    maintainer_email='',
    license='BSD',
    py_modules=['intake_questgdal'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['intake', 'rasterio', 'xarray'],
    long_description="",
    zip_safe=False,
)
