import os
import pandas as pd
import xarray as xr
import numpy as np

model_output_dir = "/lustre/nobackup/WUR/ESG/zhou111/WOFOST-Nutrient/CaseStudy/Yangtze/Output/Output_Yp"
output_path = "/lustre/nobackup/WUR/ESG/zhou111/Model_Results/1_Yp_WOFOST/Yangtze"

crop_types = ["mainrice"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]

for crop in crop_types:
    # Read the file
    model_result = os.path.join(model_output_dir, f"{crop}_Yp_1985-2014.csv")
    df = pd.read_csv(model_result)

    # Get the row with the highest average yield
    max_yield_per_pixel = df.loc[df.groupby(['Lat', 'Lon'])['Avg'].idxmax()]

    Yp_data = max_yield_per_pixel[['Lat', 'Lon', 'SowingDay', 'GrowingDays', 'TSM1', 'TSM2', 'Avg']]

    lat = np.unique(Yp_data['Lat'])
    lon = np.unique(Yp_data['Lon'])

    # Create empty arrays for the variables we want to save
    TSM1 = np.full((len(lat), len(lon)), np.nan)
    TSM2 = np.full((len(lat), len(lon)), np.nan)
    Yp = np.full((len(lat), len(lon)), np.nan)
    Sow_date = np.full((len(lat), len(lon)), np.nan)
    Growing_length = np.full((len(lat), len(lon)), np.nan)

    for idx, row in Yp_data.iterrows():
        lat_idx = np.where(lat == row['Lat'])[0][0]
        lon_idx = np.where(lon == row['Lon'])[0][0]
        
        TSM1[lat_idx, lon_idx] = row['TSM1']
        TSM2[lat_idx, lon_idx] = row['TSM2']
        Yp[lat_idx, lon_idx] = row['Avg']
        Sow_date[lat_idx, lon_idx] = row['SowingDay']
        Growing_length[lat_idx, lon_idx] = row['GrowingDays']

    # Create an xarray Dataset
    ds = xr.Dataset(
        {
            'TSUM1': (['lat', 'lon'], TSM1),
            'TSUM2': (['lat', 'lon'], TSM2),
            'Potential_Yield_WOFOST': (['lat', 'lon'], Yp),
            'Sow_date': (['lat', 'lon'], Sow_date),
            'Growing_length':(['lat', 'lon'], Growing_length)
        },
        coords={
            'lat': lat,
            'lon': lon,
        }
    )

    ds['Potential_Yield_WOFOST'].attrs['units'] = 'kg/ha'
    ds['Sow_date'].attrs['units'] = 'dekad'
    ds['Growing_length'].attrs['units'] = 'days'
 
    output_ncfile = os.path.join(output_path, f"{crop}_Yp_his.nc")
    # Save the Dataset to a NetCDF file
    ds.to_netcdf(output_ncfile)

    print(f"{output_ncfile} has been created")