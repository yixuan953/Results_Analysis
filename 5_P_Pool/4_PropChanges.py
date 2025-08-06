import pandas as pd
import matplotlib.pyplot as plt
import os

# ---- CONFIG ----
input_dir = '/lustre/nobackup/WUR/ESG/zhou111/WOFOST-NPcycling/Output'
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_P_dynamics'
variables = ['P_Uptake', 'P_Leaching', 'P_Sub', 'P_Surf']
colors = ['red', 'green', 'orange', 'blue']

# Selected pixels (1 per basin)
selected_points = {
    'Yangtze': (30.25, 112.25),
    'LaPlata': (-33.25, -59.75),
    'Rhine': (49.25, 7.75),
    'Indus': (29.25, 70.75)
}

# ---- PROCESS EACH POINT ----
for basin, (lat, lon) in selected_points.items():
    csv_path = os.path.join(input_dir, f'{basin}_wnl_withIrri_maize_Daily.csv')
# ---- LOAD & CLEAN ----
    df = pd.read_csv(csv_path, low_memory=False)
    for var in variables:
        df[var] = pd.to_numeric(df[var], errors='coerce')
    df_point = df[(df['Lat'] == lat) & (df['Lon'] == lon)].copy()
    
    # Calculate annual sums
    annual = df_point.groupby('Year')[variables].sum()

    # ---- PLOT ----
    fig, ax = plt.subplots(figsize=(10, 6))

    bottom = None
    for var, color in zip(variables, colors):
        ax.bar(annual.index, annual[var], bottom=bottom, label=var.replace('_', ' '), color=color)
        bottom = annual[var] if bottom is None else bottom + annual[var]

    ax.set_title(f'Annual P Flows at Selected Pixel in {basin} Basin\n(Lat={lat}, Lon={lon})')
    ax.set_xlabel('Year')
    ax.set_ylabel('P Fluxes (kg/ha)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/{basin}_Pillar_PFluxes.png", dpi=300)
    plt.close()