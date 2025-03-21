# This code is used to exclude unreasonabel pixels from the original output of WOFOST
# 1. For mainrice: 
#    - Potential yield > 3500 kg/ha
#    - Growing days < 180 days
# 2. For Second rice: 
#    - Potential yield > 3500 kg/ha
#    - Growing days < 140 days

import os
import xarray as xr
import numpy as np

StudyAreas = ["Rhine"] # ["Rhine", "Yangtze", "LaPlata", "Indus"]
crop_types = ["soybean"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]

for StudyArea in StudyAreas:
   input_dir = f"/lustre/nobackup/WUR/ESG/zhou111/Model_Results/1_Yp_WOFOST/{StudyArea}"
   output_dir = f"/lustre/nobackup/WUR/ESG/zhou111/Model_Results/1_Yp_WOFOST/{StudyArea}"

   for crop in crop_types:
      # Read the file
      model_result = os.path.join(input_dir, f"{crop}_Yp_his_org.nc")
      ds = xr.open_dataset(model_result)

      for var in ds.data_vars:
            if np.issubdtype(ds[var].dtype, np.timedelta64):
               ds[var] = ds[var].dt.total_seconds() / (60 * 60 * 24)  # Convert to days
      
      if crop == "mainrice":
         mask = (ds["Growing_length"] >= 170) | (ds["Potential_Yield_WOFOST"] < 3500) | (ds["Potential_Yield_WOFOST"] > 14000)
      
      if crop == "secondrice":
         mask = (ds["Growing_length"] >= 140) | (ds["Potential_Yield_WOFOST"] < 3500) | (ds["Potential_Yield_WOFOST"] > 14000)

      if crop == "winterwheat":
         mask = (ds["Growing_length"] >= 270) | (ds["Potential_Yield_WOFOST"] < 3500) | (ds["Potential_Yield_WOFOST"] > 14000)

      if crop == "maize":
         mask = (ds["Growing_length"] >= 130) | (ds["Potential_Yield_WOFOST"] < 3500) | (ds["Potential_Yield_WOFOST"] > 15000)

      if crop == "soybean":
         mask = (ds["Growing_length"] >= 160) | (ds["Potential_Yield_WOFOST"] < 1000) | (ds["Potential_Yield_WOFOST"] > 4000)

      if crop == "springwheat":
         mask = (ds["Growing_length"] >= 300) | (ds["Potential_Yield_WOFOST"] < 3500) | (ds["Potential_Yield_WOFOST"] > 14000)

      ds_filtered = ds.where(~mask, other=np.nan)  # Change `np.nan` to -9999 if needed

      output_file = os.path.join(output_dir, f"{crop}_Yp_his.nc")
      ds_filtered.to_netcdf(output_file)
      
      print(f"{output_file} has been created")