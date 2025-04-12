# This code is used to plot the irrigation rate for main crops

import os
import xarray as xr
import matplotlib.pyplot as plt
import calendar
import numpy as np

input_dir = "/lustre/nobackup/WUR/ESG/zhou111/Data/Irrigation/CaseStudy"
StudyArea = "Yangtze"
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat"]
plot_year = 2000
output_dir="/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_Irri"

for Crop in crop_types:

    # Get the irrigation rate and deal with the missing value
    Irri_File = os.path.join(input_dir, f"{StudyArea}_{Crop}_monthly_Irri_Rate.nc")
    data_irri = xr.open_dataset(Irri_File)
    Irri_Rate = data_irri.sel(year=plot_year)["Irrigation_Rate"]

    fill_value = Irri_Rate.attrs.get('_FillValue', None)
    if fill_value is not None:
        Irri_Rate = Irri_Rate.where((Irri_Rate != 0) & (Irri_Rate != fill_value), np.nan)
    else:
        Irri_Rate = Irri_Rate.where((Irri_Rate != 0) & np.isfinite(Irri_Rate), np.nan)

    # Set up subplot grid: 3 rows × 4 columns
    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 10), constrained_layout=True)
    axes = axes.ravel()  # Flatten to easily index with month number

    vmin = float(Irri_Rate.min().values)
    vmax = float(Irri_Rate.max().values)

    for month in range(1, 13):
        ax = axes[month - 1]
        irri_month = Irri_Rate.sel(month=month)
        im = irri_month.plot(ax=ax, cmap="YlGnBu", vmin=vmin, vmax=vmax, add_colorbar=False)
        ax.set_title(calendar.month_name[month])
        ax.set_xlabel("")
        ax.set_ylabel("")

    # Add one shared colorbar
    cbar = fig.colorbar(im, ax=axes.tolist(), orientation="horizontal", fraction=0.05, pad=0.05)
    cbar.set_label("Irrigation Rate [mm]")

    fig.suptitle(f"{Crop.capitalize()} Monthly Irrigation Rate - {plot_year}", fontsize=16)
    plot_path = os.path.join(output_dir, f"{StudyArea}_{Crop}_Monthly_Irrigation.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()