#MERRA2 Data Retrieval Algorithm
# Wildcard method to select all local files
vn=xarray.open_mfdataset('path to your netcdf files/*.nc4', parallel=True)

#Isolating Precipitation & time data (checking its size)
timedata=vn.variables['time'][:].size
Rain=vn.variables['TPRECMAX'][:]

#Define Latititude and Longitude Array
lat=vn.variables['lat'][:]
lon=vn.variables['lon'][:]

#Location selected at Irvine using Google Earth Pro Application
lat_irvine= 55.6113
lon_irvine= -4.6857

#Finding the points within the data that is closest to the given Irvine coordinates
#Squared Difference is done to compensate for negative lat & lon values can be used for subtration part
sq_diff_lat= (lat-lat_irvine)**2
sq_diff_lon= (lon-lon_irvine)**2

# Selecting the data values closeest to the Irvine lat and lon coordinates
min_index_lat= sq_diff_lat.argmin()
min_index_lon= sq_diff_lon.argmin()

# Creating the time period given the file list.
# We're looking for Irvine Albedo values every Month between 2016 and 2017
import numpy as np
import pandas as pd
starting_date= '2000-1-1'
ending_date= '2020-1-1'
starting_date
date_range= pd.date_range(start = starting_date, end = ending_date,freq='M')

#Create empty data frame that uses date range as index and has another column of Albedo values called CALdata
df= pd.DataFrame(0, columns=['Rain'], index=date_range)

#Filling the dataframe with the Albedo values and checking if so
dt= np.arange(0, timedata)
for time_index in dt:
df.iloc[time_index] = Rain[time_index, min_index_lat, min_index_lon]
print(df)
break

#Create Excel File to get data from jupyter to computer
df.to_csv('Irvine_Rain.csv')

# Wildcard method to select all local files
path='Enter path to your data'
filename=glob.glob(path + '*.nc')

#Create Monthly Time stamp data compatible with temporal range of data
starting_date= '2000-1-1'
ending_date= '2018-01-1'
starting_date
date_range= pd.date_range(start = starting_date, end = ending_date,freq='M')

#Creating Empty data frame where date range is index with 2 columns of data
df= pd.DataFrame(0, columns=['LAI', 'NDVI'], index=date_range)

#Looping through all 209 Monthly Data records
for i in range (0,208):
data=netCDF4.Dataset(filename[i],'r')

#Isolating time data and checking its size
timedata=data.variables['time'][:]

#Isolating NDVI Data
NDVI=data.variables['NDVI_average'][:]

#Isolating LAI or Leaf Area index Data
LAI=data.variables['LAI_average'][:]
lat=data.variables['latitude'][:]
lon=data.variables['longitude'][:]

#Location of Interest selected at Irvine using Google Earth Pro
lat_irvine= 55.6113
lon_irvine= -4.6857

#Latitude and Longitude Index boundaries enclosing area of interest
lat1=lat[-70:-68]
lon2=lon[-370:-368]

# Selecting values closest to Lat1 & Lon2
Lat_ind=abs(lat-lat1.mean()).argmin()
Lon_ind=abs(lon-lon2.mean()).argmin()

#Filling the dataframe with the values
dt= np.arange(0, timedata)
df.iloc[i] = (LAI[0, Lat_ind, Lon_ind], NDVI[0, Lat_ind, Lon_ind])
data.close()

#Creating Microsoft Excel file for Analysis
df.to_csv('NDVI_LAI.csv')