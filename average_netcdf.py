# list of netcdf files containing a Variable "MOD08_D3_6_1_Cloud_Fraction_Day_Mean"
# want to perform some analysis on these files
# and then output to a new netcdf file with the same dimensions and headers

# import libraries
import numpy as np
import netCDF4 as nc
import os
import glob
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
# add type hints
from typing import List, Dict, Tuple, Union, Optional, Sequence, Any, Callable, TypeVar, NamedTuple, LiteralString, cast

# define function to get the data from the netcdf file
def get_data(filen: LiteralString):
    """
    Get the data from the netcdf file
    """
    # open the netcdf file
    data = nc.Dataset(filen)
    # get the data from the netcdf file
    data = data.variables['MOD08_D3_6_1_Cloud_Fraction_Day_Mean'][:]
    # return the data
    return data

all_data = []
# get the data from all the files
for filen in glob.glob('scrub*.nc'):
    all_data.append(get_data(filen))
    
# convert the list to an array  
all_data = np.array(all_data)

def analysis(data: np.ndarray):
    """
    Perform some analysis on the data
    """
    # get the mean of the data
    # mean = np.mean(data, axis=0)
    mean = np.mean(data, axis=0)
    mean = np.ma.filled(mean, fill_value=-9999.0)
    mean = np.ma.masked_equal(mean, -9999.0)
    # return the mean
    return mean

def cloud_probability(data: np.ndarray, cloud_frac: float):
    """
    Calculate the cloud probability
    P(f > cloud_frac)
    """
    # get the number of observations
    n_obs = data.shape[0]
    # get the number of observations where the cloud fraction is greater than the threshold
    n_cloud = np.sum(data > cloud_frac, axis=0)
    # calculate the cloud probability
    cloud_prob = n_cloud / n_obs
    # return the cloud probability
    return cloud_prob
    
    

# perform the analysis on the data
mean = analysis(all_data)

# create a new netcdf file
# create the netcdf file
new_netcdf = nc.Dataset('new_netcdf.nc', 'w', format='NETCDF4')
# create the dimensions
new_netcdf.createDimension('time', None)
new_netcdf.createDimension('lat', 180)
new_netcdf.createDimension('lon', 360)
# create the variables
# newVar = new_netcdf.createVariable('mean', 'f4', ('time', 'lat', 'lon'))
# create a geogreferenced variable
newVar = new_netcdf.createVariable('mean', 'f4', ('lat', 'lon'), fill_value=-9999.0)
# add the attributes
newVar.units = 'percentage'
newVar.long_name = 'Cloud Fraction'
# add the lat and lon variables
lat = new_netcdf.createVariable('lat', 'f4', ('lat',))
lon = new_netcdf.createVariable('lon', 'f4', ('lon',))
# add the attributes
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon.units = 'degrees_east'
lon.long_name = 'longitude'
# add the data to the variables
lat[:] = np.arange(-90, 90)
lon[:] = np.arange(-180, 180)

newVar[:] = mean
# close the netcdf file
new_netcdf.close()
