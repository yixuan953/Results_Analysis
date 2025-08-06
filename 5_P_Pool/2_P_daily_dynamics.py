# This code is used to plot the P fluxes for the extracted pixel in maize field of 4 basins 

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Configuration
basins = ['Yangtze', 'LaPlata', 'Rhine', 'Indus']
input_dir = '/lustre/nobackup/WUR/ESG/zhou111/WOFOST-NPcycling/Output'
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_P_dynamics'
os.makedirs(output_dir, exist_ok=True)

# Select pixels for each basin
selected_pixels = {
    'Yangtze': (30.25, 112.25),
    'LaPlata': (-33.25, -59.75),
    'Rhine': (49.25, 7.75),
    'Indus': (29.25, 70.75)
}

# Variables to plot
p_vars = ['P_Uptake', 'P_avail', 'P_Surf', 'P_Sub', 'P_Leaching']
dvs_var = 'Dev_Stage'

# Plotting loop
for basin in basins:
    print(f"Processing {basin}...")

    file_path = os.path.join(input_dir, f'{basin}_wnl_withIrri_maize_Daily.csv')
    df = pd.read_csv(file_path, skipinitialspace=True)

    # Get user-defined pixel
    lat, lon = selected_pixels[basin]
    df_pixel = df[
        (df['Lat'] == lat) &
        (df['Lon'] == lon) &
        (df['Year'] >= 2001) &
        (df['Year'] <= 2005)
    ].copy()

    if df_pixel.empty:
        print(f"No data found for {basin} at Lat={lat}, Lon={lon}. Skipping.")
        continue

    # Create date column
    df_pixel['Date'] = pd.to_datetime(df_pixel['Year'].astype(str), format='%Y') + pd.to_timedelta(df_pixel['Day'] - 1, unit='D')

    # Assume df_pixel already has 'Date' column
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # --- Subplot 1: DVS and P_avail ---
    ax1 = axs[0]
    color_dvs = 'tab:blue'
    color_pavail = 'tab:orange'

    ln1 = ax1.plot(df_pixel['Date'], df_pixel['Dev_Stage'], label='DVS', color=color_dvs)
    ax1.set_ylabel('DVS [-]', color=color_dvs)
    ax1.tick_params(axis='y', labelcolor=color_dvs)

    ax1b = ax1.twinx()
    ln2 = ax1b.plot(df_pixel['Date'], df_pixel['P_avail'], label='P_avail', color=color_pavail)
    ax1b.set_ylabel('P_avail [kg/ha]', color=color_pavail)
    ax1b.tick_params(axis='y', labelcolor=color_pavail)

    # Combine legends
    lns = ln1 + ln2
    labels = [l.get_label() for l in lns]
    ax1.legend(lns, labels, loc='upper left')
    ax1.set_title(f"{basin} Basin — DVS and P_avail")

    # --- Subplot 2: P Fluxes ---
    ax2 = axs[1]
    for var in ['P_Surf', 'P_Sub', 'P_Leaching', 'P_Uptake']:
        ax2.plot(df_pixel['Date'], df_pixel[var], label=var)

    ax2.set_ylabel('P fluxes [kg/ha]')
    ax2.set_xlabel('Year')
    ax2.legend(loc='upper left')
    ax2.set_title(f"{basin} Basin — P Fluxes")

    # --- Format x-axis to show only years ---
    for ax in axs:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.grid(True)

    # --- Save figure ---
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{basin}_P_fluxes_and_DVS_split.png", dpi=300)
    plt.close()