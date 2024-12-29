### ANNEX 3 – ACCESS AND VISUALIZATION ROUTINE (AEROSOL TYPING) ###
#
# Original code: Benedetto De Rosa
# Porting, refactoring and exstension: Emilio Lapenna
# v 2.0 - 19-12-2024
#
# Reference API: https://cds.climate.copernicus.eu/how-to-api
#

import os, sys
import yaml
import zipfile
import argparse
from os.path import exists
import datetime as dt
#from datetime import timedelta

import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
#from PIL import Image

from get_data import get_data


# *** Var settings *** #
data_path = './data/'
graph_path = './graphs/'
variab_conf = 'config.yaml'
extension = 'webp' # gif, webp

# Test url-key
url = 'https://ads.atmosphere.copernicus.eu/api'
key = 'c8336150-1131-4a9a-96d1-fc80e9fd034d'


# Convert timestamp to date
def serial_date_to_string(srl_no):
    #new_date = dt.datetime(1900,1,1,0,0,0) + dt.timedelta(hours=int(srl_no)) # hours = srl_no) # OLD
    new_date = dt.datetime.fromtimestamp(int(srl_no))
    return new_date.strftime("%Y%m%d %H:00") # Artificial 00 minutes

# Read config file
def read_yaml(conf_file):
    with open(conf_file, 'r') as f:
        cnfg = yaml.load(f, Loader=yaml.SafeLoader)
    return cnfg

# Ani generator
def generate_ani(cnfg, data_path, graph_path, file_name, target, startdate, enddate, geoarea):
    # Open the NetCDF file in read mode
    dataset = nc.Dataset(data_path+file_name+'.nc', 'r')

    """
    print(dataset)
    for item in dataset.variables:
        print(item)
    sys.exit()
    """

    # Extract the latitude and longitude variables (+ time)
    latitudes = dataset.variables['latitude'][:]
    longitudes = dataset.variables['longitude'][:]
    times = dataset.variables['valid_time'][:]

    times = times.tolist() # https://numpy.org/doc/stable/reference/generated/numpy.ma.MaskedArray.tolist.html

    # Apply function to each element of list
    dates = list(map(serial_date_to_string, times))

    """
    i = 0
    for step in times:
        dates[i] = serial_date_to_string(int(step))
        i += 1
        print(dates)
    """

    print('Available frames in data file [00,03,06,09,12,15,18,21]: ', len(dates))
    print('Data file start: ', min(dates))
    print('Data file end: ', max(dates))
    #print(type(dates))


    # Extract the data from a specific variable (e.g., 'omaod550')
    aerosol_data = dataset.variables[ cnfg[int(target)]['var'] ][:, :, :] # 70

    """
    for i in range(0,1):
        print(i,' - ',aerosol_data[i, :, :].tolist())
        print("Min: ", min(aerosol_data[i, :, :].any().tolist()))
        print("Max: ", max(aerosol_data[i, :, :].any().tolist()))
    sys.exit()
    """
    """
    print('Available OD data: ', len(aerosol_data[0, :, :]))
    print(min(aerosol_data[0, :, :].all()))
    print(max(aerosol_data[0, :, :].all()))
    sys.exit()
    """

    # Number of time steps
    num_time_steps = aerosol_data.shape[0]
    print('Available measures for date range: ', num_time_steps)

    # Start building animation...
    print('Animation building... please wait...')

    # Custom limits for the logarithmic scale
    vmin_custom = float(cnfg[int(target)]["range"][0]) # Limit taken from config file
    vmax_custom = float(cnfg[int(target)]["range"][1]) # Limit taken from config file

    # Create the map using cartopy and matplotlib
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(8, 7))
    c = ax.pcolormesh(longitudes, latitudes, aerosol_data[0, :, :], shading='auto', cmap='Reds', vmin=vmin_custom, vmax=vmax_custom)
    ax.gridlines(edgecolor='gray', alpha=0.5)
    ax.coastlines(resolution='50m')
    ax.add_feature(cfeature.BORDERS) # linestyle='dotted'

    # Add state provinces to map
    #states_provinces = cfeature.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lines', scale='50m', facecolor='none')
    #ax.add_feature(states_provinces, edgecolor='gray')


    # Coordinates Italy, Europe and Eu+Af+Am regions
    # [lon_min, lon_max, lat_min, lat_max]
    italy_bounds = [5, 20, 35, 50] # Italy
    europe_bounds = [-20, 50, 20, 70] # Europe
    euafam_bounds = [-150, 80, -30, 150] # EuAfAm [-150, -30, -30, 150] & [-30, 80, 35, 110]

    if str(geoarea) == 'italy':
        map_boundaries = italy_bounds
    elif str(geoarea) == 'europe':
        map_boundaries = europe_bounds
    elif str(geoarea) == 'euafam':
        map_boundaries = euafam_bounds
    else:
        map_boundaries = italy_bounds


    # Set the limits of the x and y axis for accounting of map region
    ax.set_xlim(map_boundaries[0], map_boundaries[1])
    ax.set_ylim(map_boundaries[2], map_boundaries[3])

    #ax.set_title(f'Organic Matter Aerosol Optical Depth at 550 nm', fontsize=10, y=0.75, pad=0.25)

    # Add a sidebar for the legend
    cb = plt.colorbar(c, label='', orientation='horizontal', location='bottom', shrink=0.9) # fraction=0.055, pad=0.10) # Organic Matter AOD (550nm)


    #plt.tight_layout() # Cut white space around plots

    """
    plt.tight_layout() # Cut white space around plots
    plt.savefig('./foo.png')
    sys.exit()
    """

    # Update function for the animation
    def update(frame):
        c.set_array(aerosol_data[frame, :, :].flatten())
        # Extract the date corresponding to the frame
        current_date = dates[frame]
        #print(current_date)
        # Format the date with a comprehensible format (you can customize the format)
        formatted_date = f"{current_date[:4]}-{current_date[4:6]}-{current_date[6:]}"
        # Update the title with the description and the date
        ax.set_title(str(cnfg[int(target)]["label"])+f' - {formatted_date}', fontsize=10, ha='center', va='bottom') , # y=0.75, pad=0.25) # Set title position
        return c

    # Name of the output file with .gif extension
    output_file = cnfg[int(target)]["var"].upper()+'_'+(str(min(dates)).split(':',1)[0]).replace(' ','_')+'_'+(str(max(dates)).split(':',1)[0]).replace(' ','_')+'_'+str(geoarea)+'.'+extension

    # Create the animation
    ani = animation.FuncAnimation(fig, func=update, frames=num_time_steps, interval=200, blit=False, repeat=False)

    # Show the animation on screen
    #plt.show()

    # Remove old file if any
    if exists(graph_path+output_file):
        os.remove(graph_path+output_file)

    # Save the animation as a GIF file
    ani.save(graph_path+output_file, writer='pillow', fps=8, dpi=300)

    # Close the dataset
    dataset.close()



print('#####################################################')
print('#                                                   #')
print('#    COPERNICUS observable visualization routine    #')
print('#                                                   #')
print('#####################################################')


if __name__ == "__main__":

    def parse_args():
        """
        Parses command-line arguments for...

        Returns:
            argparse.Namespace: Parsed command-line arguments
        """
        parser = argparse.ArgumentParser(description="""
        Download data from Copernicus data service and produce animation for a specific variable.
        Arguments:\n
            target (int): Target variable to download.\n
            startdate (str): Start date in format YYYY-MM-DD.\n
            enddate (str): End date in format YYYY-MM-DD.\n
            geoarea (str): Geographical area to plot (Italy, Europe, EuAfAm).\n
            cdsapikey (str): Copernicus API key.\n

        Example usage:\n
            python3 aeflow.py --target black_carbon_aerosol_optical_depth_550nm --startdate 2022-12-01 --enddate 2022-12-03 --geoarea europe --cdsapikey 00000000-0000-0000-0000-000000000000
        """)

        parser.add_argument('--target', type=int, help='Target variable')
        parser.add_argument('--startdate', type=str, help='Start date')
        parser.add_argument('--enddate', type=str, help='End date')
        parser.add_argument('--geoarea', type=str, help='Geographical area')
        parser.add_argument('--cdsapikey', type=str, help='Copernicus API key', required=False)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        return parser.parse_args()

    args = parse_args()


# Check working directory, if any
if not data_path:
    os.makedirs(data_path)
if not graph_path:
    os.makedirs(graph_path)

# Read variable config file
cnfg = read_yaml(variab_conf)
#print(cnfg)


# Checking right option...
if int(args.target) not in range (1, len(cnfg)):
    print("You must enter a number within 1 and ",len(cnfg))
    sys.exit(1)

# Checking right option...
if not dt.datetime.strptime(args.startdate, "%Y-%m-%d"):
    sys.exit(1)

# Checking right option...
if not dt.datetime.strptime(args.enddate, "%Y-%m-%d"):
    sys.exit(1)


# Set output file name (no extension)
file_name = str(cnfg[int(args.target)]["str"]+'_'+args.startdate+'_'+args.enddate)


# Check data file
if exists(data_path+file_name+'.zip'):
    print(f'The file {file_name} exists')
else:
    print(f'The file {file_name} does not exist!')
    get_data(str(cnfg[int(args.target)]["str"]), args.startdate, args.enddate, data_path, url, args.cdsapikey)


# Check data file format (mv to netcdf)
if not exists(data_path+file_name+'.nc'):
    print("Extracting file...")
    with zipfile.ZipFile(data_path+file_name+'.zip', 'r') as zip:
        zip.extractall(data_path)
        zip.close()
    os.rename(data_path+'data_sfc.nc', data_path+file_name+'.nc')


# Generate animation
ani = generate_ani(cnfg, data_path, graph_path, file_name, args.target, args.startdate, args.enddate, args.geoarea)


#