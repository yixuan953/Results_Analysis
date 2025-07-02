# This code is used to analyze:
# 1. From 1985 - 2014, how did the range of rice field that limited by water change?
# 2. From 1985 - 2014, how did irrigation improve this?

import os
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


def csv_to_xarray(csv_path, variables=None):
    """
    Reads a CSV file with columns Lat, Lon, Year, and variables,
    converts Year and Day to datetime,
    and returns an xarray.Dataset with dimensions (time, lat, lon).
    
    Returns:
        xr.Dataset: Dataset with dims time, lat, lon and data variables.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")

    df = pd.read_csv(csv_path)

    if variables is None:
        variables = ['Storage', 'GrowthDay', 'N_Uptake', 'P_Uptake', 'N_grain', 'P_grain', 'N_Residue', 'P_Residue']

    # Sort and get unique coordinates
    lats = np.sort(df['Lat'].unique())
    lons = np.sort(df['Lon'].unique())
    times = np.sort(df['Year'].unique())

    # Map lat/lon/time values to indices in sorted arrays
    lat_idx = np.searchsorted(lats, df['Lat'])
    lon_idx = np.searchsorted(lons, df['Lon'])
    time_idx = np.searchsorted(times, df['Year'])

    data_vars = {}
    for var in variables:
        data = np.full((len(times), len(lats), len(lons)), np.nan)
        data[time_idx, lat_idx, lon_idx] = df[var].values
        data_vars[var] = (['time', 'lat', 'lon'], data)

    ds = xr.Dataset(
        data_vars=data_vars,
        coords={
            'time': times,
            'lat': lats,
            'lon': lons,
        }
    )

    return ds

StudyAreas = ["Rhine"] # ["Rhine", "Yangtze", "LaPlata", "Indus"]
crop_types = ["maize","winterwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]
periods = {
            '1985-1994': slice('1985', '1994'),
            '1995-2004': slice('1995', '2004'),
            '2005-2014': slice('2005', '2014'),
        }
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_WL"

for StudyArea in StudyAreas:
    for crop in crop_types:
        Yp_dir = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/Output/{StudyArea}_Yp_{crop}_Annual.csv"
        Wl_noIrri_dir = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/Output/{StudyArea}_wl_noIrri_{crop}_Annual.csv"
        Wl_withIrri_dir = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/Output/{StudyArea}_wl_withIrri_{crop}_Annual.csv"

        Yp = csv_to_xarray(Yp_dir, variables=None)
        Wl_noIrri = csv_to_xarray(Wl_noIrri_dir, variables=None)
        Wl_withIrri = csv_to_xarray(Wl_withIrri_dir, variables=None)

        gap_wl = 100*(Yp["Storage"] - Wl_noIrri["Storage"])/Yp["Storage"]
        gap_irri = 100*(Yp["Storage"] - Wl_withIrri["Storage"])/Yp["Storage"]

        avg_gaps_wl = {}
        avg_gaps_irri = {}
        avg_Yp = {}
        
        # Calculate the average differences in each period
        for period_name, period_slice in periods.items():
            avg_Yp[period_name] = Yp.sel(time=period_slice).mean(dim='time')
            avg_gaps_wl[period_name] = gap_wl.sel(time=period_slice).mean(dim='time')
            avg_gaps_irri[period_name] = gap_irri.sel(time=period_slice).mean(dim='time')

        # Plot 
        fig, axes = plt.subplots(1, 3, figsize=(21, 4))
        for ax, (period_name, avg_Yp) in zip(axes, avg_Yp.items()):
            im = avg_Yp["Storage"].plot(ax=ax, cmap='Oranges', vmin=0, vmax=np.nanmax(abs(avg_Yp["Storage"])), add_colorbar=False)
            ax.set_title(f'{period_name}')
            ax.set_xlabel('Lon')
            ax.set_ylabel('Lat')
        fig.suptitle(f'Potential yield of {crop} in {StudyArea} river basin [kg/ha]', fontsize=16)
        plt.tight_layout(rect=[0, 0, 0.98, 0.95])  # leave space for suptitle
        cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.85, label='Potential yield[kg/ha]')
        output_path = os.path.join(output_dir, f"{StudyArea}_{crop}_potential_yield.png")
        fig.savefig(output_path, dpi=300)

        fig, axes = plt.subplots(1, 3, figsize=(21, 4))
        for ax, (period_name, avg_gaps_wl) in zip(axes, avg_gaps_wl.items()):
            im = avg_gaps_wl.plot(ax=ax, cmap='Blues', vmin=0, vmax=np.nanmax(abs(avg_gaps_wl)), add_colorbar=False)
            ax.set_title(f'{period_name}')
            ax.set_xlabel('Lon')
            ax.set_ylabel('Lat')
        fig.suptitle('(Yp - Water-limited yield without irrigation)/Yp ', fontsize=16)
        plt.tight_layout(rect=[0, 0, 0.98, 0.95])  # leave space for suptitle
        cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.85, label='Yield gap [%]')
        output_path = os.path.join(output_dir, f"{StudyArea}_{crop}_Yp-wl.png")
        fig.savefig(output_path, dpi=300)

        fig, axes = plt.subplots(1, 3, figsize=(21, 4))
        for ax, (period_name, avg_gaps_irri) in zip(axes, avg_gaps_irri.items()):
            im = avg_gaps_irri.plot(ax=ax, cmap='Blues', vmin=0, vmax=np.nanmax(abs(avg_gaps_irri)), add_colorbar=False)
            ax.set_title(f'{period_name}')
            ax.set_xlabel('Lon')
            ax.set_ylabel('Lat')
        fig.suptitle('(Yp - Water-limited yield with irrigation)/Yp ', fontsize=16)
        plt.tight_layout(rect=[0, 0, 0.98, 0.95])  # leave space for suptitle
        cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.85, label='Yield gap [%]')
        output_path = os.path.join(output_dir, f"{StudyArea}_{crop}_Yp-wl-irri.png")
        fig.savefig(output_path, dpi=300)   