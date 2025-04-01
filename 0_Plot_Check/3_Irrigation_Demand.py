import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import calendar
import numpy as np

StudyArea = "Yangtze"
Crop = "maize"

input_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Hydro" # EvaTrans
daily_deifict = os.path.join(input_dir, f"{StudyArea}_{Crop}_Deficit_daily.nc")
monthly_deifict = os.path.join(input_dir, f"{StudyArea}_{Crop}_Deficit_monthly.nc")

data_Daily = xr.open_dataset(daily_deifict)
ds_daily = data_Daily["EvaTrans"].sel(lat=30.25, lon=107.25, method="nearest")
daily_median = ds_daily.groupby("time.dayofyear").median()

data_Monthly = xr.open_dataset(monthly_deifict)
ds_monthly = data_Monthly["EvaTrans"].sel(lat=30.25, lon=107.25, method="nearest")
monthly_mean = ds_monthly.groupby("time.month").mean()
monthly_min = ds_monthly.groupby("time.month").min()
monthly_max = ds_monthly.groupby("time.month").max()

# **Plot Daily and Monthly Data**
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# **Daily Mean Plot**
daily_median_smooth = daily_median.rolling(dayofyear=5, center=True).mean()
ax[0].plot(daily_median_smooth.dayofyear, daily_median_smooth, color="b", label="Smoothed evapotranspiration - precipitation")
ax[0].set_xlabel("Day of Year")
ax[0].set_ylabel("[mm]")
ax[0].set_title(f"Median daily evapotranspiration - precipitation \nfor {Crop} (30.25 N, 107.25 E)")
ax[0].grid(True)
ax[0].legend()

# Define all months (1-12)
all_months = np.arange(1, 13)

# Ensure monthly_mean, monthly_min, and monthly_max have all months
monthly_mean = monthly_mean.reindex(month=all_months)
monthly_min = monthly_min.reindex(month=all_months)
monthly_max = monthly_max.reindex(month=all_months)

# Plot
ax[1].plot(all_months, monthly_mean, color="g", label="Evapotranspiration - Precipitation")
ax[1].fill_between(all_months, monthly_min, monthly_max, color="lightgreen", alpha=0.5)

ax[1].set_xticks(all_months)  # Ensure all months are shown
ax[1].set_xticklabels(calendar.month_abbr[1:])  # 'Jan', 'Feb', ..., 'Dec'

ax[1].set_xlabel("Month")
ax[1].set_ylabel("[mm]")
ax[1].set_title(f"Monthly evapotranspiration - precipitation \nfor {Crop} (30.25 N, 107.25 E)")
ax[1].grid(True)
ax[1].legend()

# **Save the Plot**
output_plot = f"/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_Irri/{StudyArea}_{Crop}_EvaTrans-Prec.png"
plt.savefig(output_plot, dpi=300, bbox_inches="tight")

plt.show()
print(f"Plot saved at {output_plot}")