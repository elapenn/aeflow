#!/usr/bin/python3
#
# Reference API: https://cds.climate.copernicus.eu/how-to-api
#

import sys
import cdsapi

def get_data(variable, sdate, edate, data_path, url=None, key=None):

    # Script name sys.argv[0]
    #variable = str(sys.argv[1])
    #sdate = str(sys.argv[2])
    #edate = str(sys.argv[3])

    """
    print('############################################')
    print('Variable: '+variable)
    print('Start date: '+sdate+', End date: '+edate)
    print('############################################')
    """

    print('Downloading data... please wait...')

    dataset = "cams-global-reanalysis-eac4"
    request = {
        "variable": [variable],
        "date": [sdate+'/'+edate],
        "time": [
            "00:00", "03:00",
            "06:00", "09:00",
            "12:00", "15:00",
            "18:00", "21:00"
        ],
        "data_format": "netcdf_zip"
    }

    target = data_path+variable+'_'+sdate+'_'+edate+'.zip'

    client = cdsapi.Client(url, key)
    client.retrieve(dataset, request, target)


"""
# Test url-key
url='https://ads.atmosphere.copernicus.eu/api'
key='c8336150-1131-4a9a-96d1-fc80e9fd034d'

get_data('black_carbon_aerosol_optical_depth_550nm', '2022-01-15', '2022-01-20', './data', url, key)
"""
#
