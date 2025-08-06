# This code is used to plot the P pool changes of the 4 basin

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

input_dir = "/lustre/nobackup/WUR/ESG/zhou111/WOFOST-NPcycling/Output"
shp_base = "/lustre/nobackup/WUR/ESG/zhou111/Data/Case_Study/shp"
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_P_dynamics"
os.makedirs(output_dir, exist_ok=True)

basins = ['Yangtze', 'LaPlata', 'Rhine', 'Indus']
variables = ['Lpool', 'Spool']

def plot_variable(varname):
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(18, 20),
                             subplot_kw={'projection': ccrs.PlateCarree()})
    fig.suptitle(f"{varname} [mmol/kg soil] in 1981 vs 2010 (with % Change)", fontsize=18)

    for i, basin in enumerate(basins):
        print(f"Processing {basin} for {varname}...")

        # Load CSV
        csv_path = os.path.join(input_dir, f'{basin}_wnl_withIrri_maize_Daily.csv')
        df = pd.read_csv(csv_path, skipinitialspace=True)

        # Filter Day 1 of 1981 and 2010
        df_1981 = df[(df['Year'] == 1981) & (df['Day'] == 1)]
        df_2010 = df[(df['Year'] == 2010) & (df['Day'] == 1)]

        # Pivot to 2D grid (lat x lon)
        def grid(df, var):
            return df.pivot(index='Lat', columns='Lon', values=var).sort_index(ascending=True)

        # Skip if missing data
        if df_1981.empty or df_2010.empty:
            print(f"Skipping {basin} - {varname}: No data for 1981 or 2010 Day 1")
            continue

        # Pivot
        data1981 = grid(df_1981, varname)
        data2010 = grid(df_2010, varname)

        # Also skip if grid is empty (no lat/lon data)
        if data1981.empty or data2010.empty:
            print(f"Skipping {basin} - {varname}: Pivot returned empty data")
            continue

        # Compute % change
        change = (data2010 - data1981) / data1981.replace(0, np.nan) * 100

        # Load shapefile
        shp_path = os.path.join(shp_base, basin, f'{basin}.shp')
        gdf = gpd.read_file(shp_path)

        # Plot 3 subplots for this basin
        titles = ['1981', '2010', '% Change']
        datasets = [data1981, data2010, change]
        cmaps = ['viridis', 'viridis', 'bwr']
        vmins = [None, None, -100]
        vmaxs = [None, None, 100]

        for j in range(3):
            ax = axes[i, j]
            im = ax.pcolormesh(datasets[j].columns, datasets[j].index, datasets[j].values,
                               shading='auto', cmap=cmaps[j],
                               vmin=vmins[j], vmax=vmaxs[j])
            gdf.boundary.plot(ax=ax, edgecolor='black', linewidth=1)
            ax.set_title(f"{basin} - {varname} {titles[j]}", fontsize=10)
            ax.coastlines()
            ax.add_feature(cfeature.BORDERS, linewidth=0.5)
            fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.6)

    # Save figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_path = os.path.join(output_dir, f'{varname}_Change_1981_2010.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

for var in variables:
    plot_variable(var)