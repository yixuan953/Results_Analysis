import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import cartopy.feature as cfeature

Yp_dir = "/lustre/nobackup/WUR/ESG/zhou111/Model_Results/1_Yp_WOFOST"
shp_path = "/lustre/nobackup/WUR/ESG/zhou111/Data/Case_Study/shp"
output_path = "/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_YP_HA"
StudyAreas = ["Rhine", "Yangtze", "LaPlata", "Indus"] # ["Rhine", "Yangtze", "LaPlata", "Indus"]
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat"] # ["maize","mainrice","secondrice","soybean","winterwheat","springwheat"]

for StudyArea in StudyAreas:
    boundary = os.path.join(shp_path, f"{StudyArea}/{StudyArea}.shp")
    shape_feature = ShapelyFeature(Reader(boundary).geometries(), ccrs.PlateCarree(), edgecolor="red", facecolor="none")

    for crop in crop_types:
        # Read the file
        model_result = os.path.join(Yp_dir, f"{StudyArea}/{StudyArea}_{crop}_Yp_mask.nc")
        
        if not os.path.exists(model_result):
            print(f"File not found: {model_result}, skipping...")
            continue

        ds = xr.open_dataset(model_result)
        HA = ds["HA"]
        Yp = ds["Yp"]

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), subplot_kw={"projection": ccrs.PlateCarree()})

        # Define a function to plot data
        def plot_variable(ax, data, title):
            data.plot(ax=ax, cmap="viridis", transform=ccrs.PlateCarree())
            ax.add_feature(shape_feature, linewidth=1.5)
            ax.add_feature(cfeature.COASTLINE, linewidth=1)
            ax.add_feature(cfeature.BORDERS, linestyle=":")
            ax.set_title(title)

        # Plot both variables
        plot_variable(axes[0], HA, f"Havested area [ha] of {crop} for {StudyArea} river basin")
        plot_variable(axes[1], Yp, f"Potential yield [kg/ha] of {crop} for {StudyArea} river basin")

        # Adjust layout
        plt.tight_layout()

        # Save as PNG file
        output_file = os.path.join(output_path, f"{StudyArea}_{crop}_Yp_HA.png")
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.show()

        print(f"Plot saved to {output_file}")