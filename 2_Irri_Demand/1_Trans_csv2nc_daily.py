# This script is used to:
# 1. Transform the daily transpiration, evaporation from .csv into .nc format
# 2. Upscale it to monthly scale and save into .nc format

import os
import pandas as pd
import xarray as xr
import numpy as np
import datetime as dt

StudyAreas = ["Rhine", "Yangtze", "LaPlata", "Indus"] # ["Rhine", "Yangtze", "LaPlata", "Indus"]
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]

for StudyArea in StudyAreas:
    meteo_data_dir = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/CaseStudy_Meteo/{StudyArea}/{StudyArea}_Prec_daily_1981-2019.nc"
    model_output_dir = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/Output"
    output_path = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/Output/Daily_nc_file"

    for crop in crop_types:
        # Read the file
        model_result = os.path.join(model_output_dir, f"{StudyArea}_Yp_{crop}_Daily.csv")

        if not os.path.exists(model_result):
            print(f"File not found: {model_result}, skipping...")
            continue
        print(f"Start to process {model_result}...")

        df = pd.read_csv(model_result)
        # Step 2: Convert Year and Day to a datetime object
        df['time'] = df.apply(lambda row: dt.datetime(int(row['Year']), 1, 1) + dt.timedelta(days=int(row['Day'])-1), axis=1)

        lats = sorted(df['Lat'].unique())
        lons = sorted(df['Lon'].unique())
        times = sorted(df['time'].unique())
        variables = ['Transpiration', 'EvaWater', 'EvaSoil', 'SoilMoisture', 'N_demand', 'P_demand', 'Dev_Stage']
        data_vars = {}

        for var in variables:
            # Initialize with NaN
            data = np.full((len(times), len(lats), len(lons)), np.nan)
            
            # Fill the array with values from the DataFrame
            for index, row in df.iterrows():
                t_idx = times.index(row['time'])
                lat_idx = lats.index(row['Lat'])
                lon_idx = lons.index(row['Lon'])
                data[t_idx, lat_idx, lon_idx] = row[var]
            
            # Add to our data variables dictionary
            data_vars[var] = (['time', 'lat', 'lon'], data)

        # Step 5: Create the xarray Dataset
        ds = xr.Dataset(
            data_vars=data_vars,
            coords={
                'time': times,
                'lat': lats,
                'lon': lons,
            },
            attrs={
                'description': 'Converted from wofost output .csv data',
                'creation_date': dt.datetime.now().strftime('%Y-%m-%d')
            }
        )

        for var in variables:
            if var == 'Transpiration':
                ds[var].attrs = {'units': 'mm/day', 'long_name': 'Crop transpiration'}
            elif var == 'EvaWater':
                ds[var].attrs = {'units': 'mm/day', 'long_name': 'Water evaporation'}
            elif var == 'EvaSoil':
                ds[var].attrs = {'units': 'mm/day', 'long_name': 'Soil evaporation'}
            elif var == 'SoilMoisture':
                ds[var].attrs = {'units': '-', 'long_name': 'Soil moisture content'}
            elif var == 'N_demand':
                ds[var].attrs = {'units': 'kg/ha', 'long_name': 'Nitrogen demand'}
            elif var == 'P_demand':
                ds[var].attrs = {'units': 'kg/ha', 'long_name': 'Phosphorus demand'}
            elif var == 'Dev_Stage':
                ds[var].attrs = {'units': '-', 'long_name': 'Development stage'}

        ds.lat.attrs = {'units': 'degrees_north', 'long_name': 'Latitude'}
        ds.lon.attrs = {'units': 'degrees_east', 'long_name': 'Longitude'}
        ds.time.attrs = {'long_name': 'Time'}

        output_ncfile = os.path.join(output_path, f"{StudyArea}_{crop}_Yp_daily.nc")
        ds.to_netcdf(output_ncfile)

        print(f"Successfully converted CSV to {output_ncfile}!")