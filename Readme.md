# COPERNICUS Climate data mapping utility

"""
https://www.markdownguide.org/basic-syntax/
"""

This utility uses Copernicus Climate data to generate animations of aerosol evolution of a physical variable on a specific area.
It is possible to plot a map for Italy [1], Europe [2] and EuAfAm [3] area.

In the file __config.yaml__ you can find physical variables to plot, the number [1,2...10] correspond to `--target` parameter:

1. black_carbon_aerosol_optical_depth_550nm
2. dust_aerosol_optical_depth_550nm
3. organic_matter_aerosol_optical_depth_550nm
4. sea_salt_aerosol_optical_depth_550nm
5. sulphate_aerosol_optical_depth_550nm
6. total_aerosol_optical_depth_469nm
7. total_aerosol_optical_depth_550nm
8. total_aerosol_optical_depth_670nm
9. total_aerosol_optical_depth_865nm
10. total_aerosol_optical_depth_1240nm

For `--startdate` and `--enddate` always use the YYYY-mm-dd formate, like 2000-01-01.

For the `--geoarea` parameter you can choose between three options: italy, europe, and euafam (always lowercase)

Copernicus Climate data will be download in __data__ directory, while animations will be generated in __graphs__ directory.

### Basic use as Python script

From your local installation you can run from terminal:

`python3 aeflow.py --target 1 --startdate 2022-12-01 --enddate 2022-12-20 --geoarea europe --cdsapikey 00000000-0000-0000-0000-000000000000`

(remember to set your own API key)

### Docker

The code has also been Dockerized, you can run:

`docker build -t aeflow .`

And run for a test example:

`docker run -v aeflow --target 1 --startdate 2022-12-01 --enddate 2022-12-03 --geoarea europe --cdsapikey 00000000-0000-0000-0000-000000000000`

(remember to set your own API key)

For `--cdsapikey` parameter you must obtain your own Copernicus Climate CDS API key.

You can register and get your personal key here: https://cds.climate.copernicus.eu/

#