import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import cartopy.feature as cfeature

res_lit_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/N_Fert_Man_Inorg_1961-2020/N_Residue_app_rate_05d"
res_wofost_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Fertilization/NP_Fert_Res"
shp_path = "/lustre/nobackup/WUR/ESG/zhou111/Data/Case_Study/shp"
output_path = "/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_Res_Comp"
StudyAreas = ["Yangtze"] # ["Rhine", "Yangtze", "LaPlata", "Indus"]
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]
plot_year = 2000

for StudyArea in StudyAreas:
    boundary = os.path.join(shp_path, f"{StudyArea}/{StudyArea}.shp")
    shape_feature = ShapelyFeature(Reader(boundary).geometries(), ccrs.PlateCarree(), edgecolor="red", facecolor="none")

    for crop in crop_types:
        # Read the wofost output .nc file
        model_result = os.path.join(res_wofost_dir, f"{StudyArea}_{crop}_Res_NP_1997-2016.nc")
        
        if not os.path.exists(model_result):
            print(f"File not found: {model_result}, skipping...")
            continue

        ds_wofost = xr.open_dataset(model_result)
        N_Res_wofost = ds_wofost.sel(year=plot_year)["N_Res_Input"]

        # Get spatial bounds from model_result
        lon_min, lon_max = ds_wofost.lon.min().item(), ds_wofost.lon.max().item()
        lat_min, lat_max = ds_wofost.lat.min().item(), ds_wofost.lat.max().item()
        print(f"lon_min = {lon_min}, lon_max = {lon_max}")
        print(f"lat_min = {lat_min}, lax_max = {lat_max}")

        # Change the crop name to match the global dataset
        if crop == "mainrice" or crop == "secondrice":
            glob_crop = "Rice"       
        if crop == "springwheat" or crop == "winterwheat":
            glob_crop = "Wheat"
        if crop == "maize":
            glob_crop = "Maize"
        if crop == "soybean":
            glob_crop = "Soybean"
        
        lit_res = os.path.join(res_lit_dir, f"N_Residue_app_rate_{glob_crop}_1961-2020.nc")
        print(f"Processing N_Residue_app_rate_{glob_crop}_1961-2020.nc")
        ds_lit = xr.open_dataset(lit_res)
        N_Res_lit = ds_lit.sel(year=plot_year)['Residue_N_application_rate']
        print(f"Shape: {N_Res_lit.shape}")
        print(f"Data type: {N_Res_lit.dtype}")

        # Crop the literature data to the same spatial extent as model result
        N_Res_lit_cropped = N_Res_lit.sel(lat=slice(lat_max,lat_min), 
                                          lon=slice(lon_min, lon_max))
        print(f"Shape: {N_Res_lit_cropped.shape}")
        print(f"Data type: {N_Res_lit_cropped.dtype}")
        
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), subplot_kw={"projection": ccrs.PlateCarree()})
        vmin = min(N_Res_wofost.min().item(), N_Res_lit_cropped.min().item())
        vmax = max(N_Res_wofost.max().item(), N_Res_lit_cropped.max().item())

        # Define a function to plot data
        def plot_variable(ax, data, title):
            im = data.plot(ax=ax, cmap="YlOrBr", transform=ccrs.PlateCarree(),vmin=vmin, vmax=vmax, add_colorbar=False)
            ax.add_feature(shape_feature, linewidth=1.5)
            ax.add_feature(cfeature.COASTLINE, linewidth=1)
            ax.add_feature(cfeature.BORDERS, linestyle=":")
            ax.set_title(title)
            return im

        # Plot both variables
        im1 = plot_variable(axes[0], N_Res_wofost, f"N residue application rate [kg/ha] of {crop} \nfor {StudyArea} river basin (wofost) in 2000")
        im2 = plot_variable(axes[1], N_Res_lit_cropped, f"N residue application rate [kg/ha] of {glob_crop} \nfor {StudyArea} river basin (Adalibieke et al., 2023) in 2000")
        # Add shared colorbar
        fig.subplots_adjust(bottom=0.2)
        # Add the colorbar axes at the bottom
        cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.03])  # [left, bottom, width, height]
        # Create the colorbar
        cbar = fig.colorbar(im2, cax=cbar_ax, orientation='horizontal', label='N Residue Application Rate [kg/ha]')
        # Save as PNG file
        output_file = os.path.join(output_path, f"{StudyArea}_{crop}_Res_Compare.png")
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.show()
        print(f"Plot saved to {output_file}")