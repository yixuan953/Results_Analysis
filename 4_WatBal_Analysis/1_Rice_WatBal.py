# This code is used to analyze:
# 1. From 1985 - 2014, what is the average annual surface runoff?
# 2. From 1985 - 2014, when did the surface runoff happen? 

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import numpy as np
import os

# === File Paths ===
csv_file = "/lustre/nobackup/WUR/ESG/zhou111/WOFOST-NPcycling/Output/Yangtze_wnl_withIrri_mainrice_Daily.csv"
boundary = "/lustre/nobackup/WUR/ESG/zhou111/Data/Case_Study/shp/Yangtze/Yangtze.shp"
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_WatBal"
output_file = os.path.join(output_dir, "Avg_Annual_SurfaceRunoff_Yangtze.png")

# === Load CSV ===
df = pd.read_csv(csv_file)

# === Process Runoff Data ===
annual_runoff = df.groupby(['Lat', 'Lon', 'Year'])['SurfaceRunoff'].sum().reset_index()
avg_annual_runoff = annual_runoff.groupby(['Lat', 'Lon'])['SurfaceRunoff'].mean().reset_index()
avg_annual_runoff['SurfaceRunoff'] *= 10  # convert to mm if needed

# === Prepare Grid ===
lats = sorted(avg_annual_runoff['Lat'].unique())
lons = sorted(avg_annual_runoff['Lon'].unique())
runoff_grid = avg_annual_runoff.pivot(index='Lat', columns='Lon', values='SurfaceRunoff').values

lon2d, lat2d = np.meshgrid(lons, lats)

# === Plot with Cartopy ===
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([min(lons), max(lons), min(lats), max(lats)], crs=ccrs.PlateCarree())

# Add shapefile
shape_feature = ShapelyFeature(Reader(boundary).geometries(), ccrs.PlateCarree(),
                                edgecolor="red", facecolor="none", linewidth=1.2)
ax.add_feature(shape_feature)

# Add coastlines/gridlines for context
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.gridlines(draw_labels=True)

# Plot the runoff data
pcm = ax.pcolormesh(lon2d, lat2d, runoff_grid, cmap="YlGnBu", shading="auto")
cbar = plt.colorbar(pcm, ax=ax, shrink=0.7, label="Avg Annual Surface Runoff (mm)")

# Title and save
plt.title("Average Annual Surface Runoff in Yangtze River Basin")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()

print(f"Map has saved to: {output_file}")
