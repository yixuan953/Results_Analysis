# This code is used to create new mask for further runs

import os
import xarray as xr
import numpy as np

StudyAreas = ["Rhine", "Yangtze", "LaPlata", "Indus"] #  ["Rhine", "Yangtze", "LaPlata", "Indus"] 
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]

for StudyArea in StudyAreas:
   org_mask_dir = f"/lustre/nobackup/WUR/ESG/zhou111/Data/Crop_Mask/CaseStudy/{StudyArea}"
   model_output_dir = f"/lustre/nobackup/WUR/ESG/zhou111/Model_Results/1_Yp_WOFOST/{StudyArea}"

   for crop in crop_types:
      # Read the file
      org_mask = os.path.join(org_mask_dir, f"{StudyArea}_{crop}_mask.nc")
      model_result = os.path.join(model_output_dir, f"{crop}_Yp_his.nc")

      if not os.path.exists(model_result):
         print(f"File not found: {model_result}, skipping...")
         continue
      
      ds_mask = xr.open_dataset(org_mask)
      ds_model = xr.open_dataset(model_result)
      
      lat_mask = ds_mask['lat']
      lon_mask = ds_mask['lon']
      lat_model = ds_model['lat']
      lon_model = ds_model['lon']

      # Mask each variable in ds_model based on the latitude and longitude range of ds_mask
      lat_min = lat_mask.min()
      lat_max = lat_mask.max()
      lon_min = lon_mask.min()
      lon_max = lon_mask.max()

      ds_model_sub = ds_model.sel(lat=slice(ds_mask.lat.min(), ds_mask.lat.max()), lon=slice(ds_mask.lon.min(), ds_mask.lon.max()))
      ds_model_aligned = ds_model_sub.reindex(lat=ds_mask.lat, lon=ds_mask.lon, method=None)
      ds_model_aligned = ds_model_aligned.fillna(np.nan)

      ds_combined = xr.Dataset(
            {
                'TSUM1': (['lat', 'lon'], ds_model_aligned['TSUM1'].values),
                'TSUM2': (['lat', 'lon'], ds_model_aligned['TSUM2'].values),
                'Yp': (['lat', 'lon'], ds_model_aligned['Potential_Yield_WOFOST'].values),
                'Sow_date': (['lat', 'lon'], ds_model_aligned['Sow_date'].values),
                'Growing_length':(['lat', 'lon'], ds_model_aligned['Growing_length'].values),
                'HA': (['lat', 'lon'], ds_mask['HA'].values) 
            },
            coords={'lat': lat_mask, 'lon': lon_mask}
        )
      
      ds_combined['HA'].attrs['units'] = 'ha'
      ds_combined['Yp'].attrs['units'] = 'kg/ha'
      ds_combined['Sow_date'].attrs['units'] = 'dekad'
      ds_combined['Growing_length'].attrs['units'] = 'days'

      # Save the combined dataset
      output_nc = os.path.join(model_output_dir, f"{StudyArea}_{crop}_Yp_mask.nc")
      ds_combined.to_netcdf(output_nc)
      print(f"{StudyArea}_{crop}_Yp_mask.nc has been saved")