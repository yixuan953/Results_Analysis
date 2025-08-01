import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# === File paths ===
csv_file = "/lustre/nobackup/WUR/ESG/zhou111/WOFOST-NPcycling/Output/Yangtze_wnl_withIrri_mainrice_Daily.csv"
output_dir = "/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_WatBal"
output_file = os.path.join(output_dir, "DevStage_SurfaceRunoff_AllPoints.png")

# === Load Data ===
df = pd.read_csv(csv_file)
df['Date'] = pd.to_datetime(df['Year'] * 1000 + df['Day'], format='%Y%j')

# === Selected Coordinates ===
selected_points = [(30.25, 107.25), (28.75, 117.25), (29.25, 113.75)]

# === Set up the figure
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14, 10), sharex=True)

for i, (lat, lon) in enumerate(selected_points):
    ax1 = axes[i]
    subset = df[(df['Lat'] == lat) & (df['Lon'] == lon)].copy()
    
    if subset.empty:
        print(f"No data found for ({lat}, {lon})")
        continue

    # Plot Dev_Stage on left y-axis
    ax1.plot(subset['Date'], subset['Dev_Stage'], color='blue', label='Dev_Stage')
    ax1.set_ylabel("Dev_Stage", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(0, 3)  # Typical DVS range

    # Plot SurfaceRunoff on right y-axis
    ax2 = ax1.twinx()
    ax2.plot(subset['Date'], subset['SurfaceRunoff'], color='green', label='SurfaceRunoff')
    ax2.set_ylabel("SurfaceRunoff (mm)", color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Title for subplot
    ax1.set_title(f"(Lat: {lat}, Lon: {lon})")

# Format x-axis to show only years
years = mdates.YearLocator()
year_fmt = mdates.DateFormatter('%Y')
axes[-1].xaxis.set_major_locator(years)
axes[-1].xaxis.set_major_formatter(year_fmt)
plt.xlabel("Year")

plt.suptitle("Development Stage and Surface Runoff at Selected Locations", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for suptitle

# Save the figure
plt.savefig(output_file, dpi=300)
plt.close()

print(f"Combined plot saved to: {output_file}")