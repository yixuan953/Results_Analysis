import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import os

# Setup
basins = ['Yangtze', 'LaPlata', 'Rhine', 'Indus']
variables = ['P_Uptake', 'P_Surf', 'P_Sub', 'P_Leaching']
var_titles = {
    'P_Uptake': 'P uptake',
    'P_Surf': 'P losses through surface runoff',
    'P_Sub': 'P losses through subsurface runoff',
    'P_Leaching': 'P losses through leaching'
}
input_dir = '/lustre/nobackup/WUR/ESG/zhou111/WOFOST-NPcycling/Output'
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_P_dynamics'

os.makedirs(output_dir, exist_ok=True)

for basin in basins:
    print(f"Processing {basin}...")

    # Load daily model output
    csv_path = os.path.join(input_dir, f"{basin}_wnl_withIrri_maize_Daily.csv")
    df = pd.read_csv(csv_path)
    for var in variables:
        df[var] = pd.to_numeric(df[var], errors='coerce')

    # Filter for 1981–2010
    df = df[(df['Year'] >= 1981) & (df['Year'] <= 2010)]
    df.dropna(subset=variables, inplace=True)

    # Convert daily values to annual totals [kg/ha/year]
    annual_sum = df.groupby(['Lat', 'Lon', 'Year'])[variables].sum().reset_index()

    # Average over years to get mean annual value [kg/ha/year]
    mean_annual = annual_sum.groupby(['Lat', 'Lon'])[variables].mean().reset_index()

    # Prepare 2D grids for plotting
    pivot_data = {}
    for var in variables:
        pivot = mean_annual.pivot(index='Lat', columns='Lon', values=var)
        pivot_data[var] = pivot.sort_index(ascending=False)  # Lat descending = north-up

    # Load basin boundary shapefile
    shp_path = f"/lustre/nobackup/WUR/ESG/zhou111/Data/Case_Study/shp/{basin}/{basin}.shp"
    basin_shp = gpd.read_file(shp_path)

    # Plot: 4 subplots in 1 figure
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    axs = axs.flatten()

    for i, var in enumerate(variables):
        ax = axs[i]
        data = pivot_data[var]
        lon = data.columns.values
        lat = data.index.values
        im = ax.pcolormesh(lon, lat, data.values, shading='auto', cmap='viridis')

        ax.set_title(var_titles[var])
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        basin_shp.boundary.plot(ax=ax, edgecolor='red', linewidth=1)

        cbar = plt.colorbar(im, ax=ax, orientation='vertical', shrink=0.8)
        cbar.set_label('kg/ha/year')

    fig.suptitle(f"{basin} Basin – Avg Annual P Flows (1981–2010)", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"{output_dir}/{basin}_P_flows_1981-2010.png", dpi=300)
    plt.close()

    print(f"Saved: {output_dir}/{basin}_P_flows_1981-2010.png")