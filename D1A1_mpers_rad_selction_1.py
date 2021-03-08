#!/usr/bin/env python3
# date:01.03.2021
# author:jonathan minz
# project:Agora Offpot-Evaluating_offshore_German_Bight_wind_energy_scenarios

# import packages 
import glob
import xarray as xr
import xarray.ufuncs as xu
import numpy as np
import pandas as pd
import os

# area of interest A1

# west_east and west_east_stag :
# model dimension (not lat-long) 
A1_mod_WE_S_L = 130
A1_mod_WE_S_R = 220

# south_north and south_north_stag :
#  model dimension (not lat-long)
A1_mod_SN_T = 140
A1_mod_SN_B = 50

# empty list  declarations
ncfiles = []


# collecting WRF filenames in a list
for file in glob.glob('compress*'):
	ncfiles.append(file)
print(len(ncfiles))

# calculate annual average hourly wind speeds
def annual_avg_hourly_ws():
	'''Average hourly windspeed for MPI DTU 2006 Agora WRF simulation.
	
	Loops over daily netcdf WRF simulation outputs to 
	Extract U and V wind speeds components at level = 6, 
	close to hub-height, destagger to mass point. Calculate
	windspeeds, and then average over grid to estimate
	average hourly wind speeds. 
	
	Parameters:
	None
	
	Returns:
	*_hourly.nc: netcdf file 
	 
	'''
	wsl = []
	d_geo = xr.open_dataset('landmask.nc')
	
	for idx, file in enumerate(ncfiles):
		ds_f = xr.open_dataset(file)
		ds_f_U = ds_f.U # extract X component of wind speeds
		ds_f_V = ds_f.V # extract y component of wind speeds
		dnx = np.shape(ds_f_U)[3] - 1
		dny = np.shape(ds_f_V)[2] - 1
		U_dstag = 0.5 * (ds_f_U[:,:,:,0:dnx] + ds_f_U[:,:,:,1:dnx+1])  # destagger X wind speeds 
		V_dstag = 0.5 * (ds_f_V[:,:,0:dny,:] + ds_f_V[:,:,1:dny+1,:])  # destagger Y wind speeds
		U_ren = U_dstag.rename({'west_east_stag':'west_east'})
		V_ren = V_dstag.rename({'south_north_stag':'south_north'})
		ws_X_sea = U_ren.sel(bottom_top = 6).where(d_geo.LANDMASK == 0)
		ws_Y_sea = V_ren.sel(bottom_top = 6).where(d_geo.LANDMASK == 0)
		ws_Y = ws_X_sea.mean(dim = ['south_north','west_east']) # calculate spatial mean of X wind speeds
		ws_X = ws_Y_sea.mean(dim = ['south_north','west_east']) # calculate spatial mean of Y wind speeds
		ws_XY = xu.sqrt(ws_X**2 + ws_Y**2) # calculate effective wind speeds 
		ws_XY.to_netcdf('s_'+str(file)+'_hourly.nc')
		
# calculate annual average hourly wind speeds for an areal selection around A1
def A1_yr_avg_hourly_ws():
    '''Average hourly windspeed for MPI DTU 2006 Agora WRF simulation.
    This function selects data over an areal selection. 
    
    # west_east and west_east_stag :
    # model dimension (not lat-long) 
    A1_mod_WE_S_L = 130
    A1_mod_WE_S_R = 220

    # south_north and south_north_stag :
    #  model dimension (not lat-long)
    A1_mod_SN_T = 140
    A1_mod_SN_B = 50
	
	Loops over daily netcdf WRF simulation outputs to 
	Extract U and V wind speeds components at level = 6, 
	close to hub-height, destagger to mass point. Calculate
	windspeeds, and then average over grid to estimate
	average hourly wind speeds. In addtion, the function also writes out
	a netcdf file with the hourly average wind directions over the selected 
    model area.
    
	Parameters:
	None
	
	Returns:
	prints *_hourly_mpers.nc: netcdf file 
    prints *_hourly_rad.nc: netcdf file
	 
	'''
	wsl = []
	d_geo = xr.open_dataset('landmask.nc')
	
	for idx, file in enumerate(ncfiles):
		ds_f = xr.open_dataset(file) 
		ds_f_U = ds_f.U.sel(south_north = slice(50,140),west_east_stag = slice(130,220))
		ds_f_V = ds_f.V.sel(south_north_stag = slice(50,140), west_east = slice(130,220))
		dnx = np.shape(ds_f_U)[3]-1
		dny = np.shape(ds_f_V)[2]-1
		U_dstag = 0.5 * (ds_f_U[:,:,:,0:dnx] + ds_f_U[:,:,:,1:dnx+1])
		V_dstag = 0.5 * (ds_f_V[:,:,0:dny,:] + ds_f_V[:,:,1:dny+1,:])
		U_ren = U_dstag.rename({'west_east_stag':'west_east'})
		V_ren = V_dstag.rename({'south_north_stag':'south_north'})
		ws_X_sea = U_ren.sel(bottom_top = 6)
		ws_Y_sea = V_ren.sel(bottom_top = 6)
		ws_X = ws_X_sea.mean(dim = ['south_north','west_east'])
		ws_Y = ws_Y_sea.mean(dim = ['south_north','west_east'])
		ws_XY = xu.sqrt(ws_X**2 + ws_Y**2)
        dir_XY = xu.arctan(ws_y/ws_x)
		ws_XY.to_netcdf('s_A1_'+str(file)+'_hourly_mpers.nc')
        dir_XY.to_netcdf('s_A1_'+str(file)+'_hourly_rad.nc')


		
# convert netcdf files to csv files 
def A1_convert_nc_to_csv():
	''' Converts nc files to csv
 	
 	Loops over annual average hourly wind speeds and direction nc files 
 	to write out .csv files with the same metrics.  
 	
 	Parameters:
 	None
 	
 	Returns:
 	*_hourly.nc.csv: csv files
	'''
	nc_to_csv_mpers = []
    nc_to_csv_rad = []
	for f in glob.glob('*_hourly_mpers.nc'):
		nc_to_csv_mpers.append(f)
    
    for i in glob.glob('*_hourly_rad.nc'):
        nc_to_csv_rad.append(i)
	
	for idx,file in enumerate(nc_to_csv_mpers):
		name = str(file)
		name = name.split('_')[5]
        direction = str(file)[:len(str(file))-8]+'rad.nc.csv'
        
		ws_file = xr.open_dataarray(str(file))
		ws_pd = ws_file.to_pandas()
		ws_pd.to_csv(str(file)+'.csv')
		open_pd = pd.read_csv(str(file)+'.csv')
		open_pd['date'] = str(name)
		open_pd.rename(columns = 
		{"0":"hourly_ms-1","Time":"Time_of_day"}, inplace = 
		True)
		open_pd.to_csv(str(file)+'.csv')
		

# Append individual  files in to one csv file
def many_to_one():
	''' Appends many csv files in to one. 
	
	Parameters: 
	None
	
	Returns:
	.csv: comma separted values file
	
	'''
	csv = []
	df_list = []
	for i in glob.glob('*_hourly.nc.csv'):
		csv.append(i)
	print(csv)
	for idx,file in enumerate(csv):
		df = pd.read_csv(file)
		df_list.append(df)
	
	one_list = pd.concat(df_list)
#	one_list.to_csv('2006_hr_avg_mpers_D1A1.csv')
	one_list.to_csv('2006_hr_yr_,mpers_selone_D1A1.csv')

def del_scratch_files():
	''' deletes all temporary files
	Parameters:
	None
	Returns:
	None
	'''
	scratch_files = []
	file_exists = []
	for i in glob.glob('*hourly*'):
		scratch_files.append(str(i))
	for idx,f in enumerate(scratch_files):
		file_exists.append(os.path.exists(f))
		os.remove(scratch_files[idx]) if file_exists[idx] == True else print('file not found')
		
	
 
# Run functions
# Select functions here which should be run

# Post processing functions

#annual_avg_hourly_ws()
#A1_yr_avg_hourly_ws()

# data manipulation
# csv output 

#convert_nc_to_csv()
many_to_one()


# housekeeping

#del_scratch_files()
	

