import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_demand_seaborn(ax, df, lat, lon):
    subset = df[(df['Lat'] == lat) & (df['Lon'] == lon)]
    
    # Plot N_demand with Seaborn, using hue for different years
    sns.lineplot(data=subset, x="Dev_Stage", y="N_demand", ax=ax, label="N_demand", color='blue', estimator="median", errorbar=("pi", 90))
    sns.lineplot(data=subset, x="Dev_Stage", y="P_demand", ax=ax, label="P_demand", color='green', estimator="median", errorbar=("pi", 90))

    ax.set_xlabel("Development Stage")
    ax.set_ylabel("Nutrient Demand [kg ha-1 day-1]")
    ax.set_title(f"N & P Demand in past 30 years(Lat: {lat}, Lon: {lon})")
    ax.legend()
    ax.grid()

# Function to plot N & P demand across all lat-lon for a fixed year
def plot_demand_year_fixed_seaborn(ax, df, year):
    subset = df[df['Year'] == year]  

    # Seaborn line plot with error bars (min-max range)
    sns.lineplot(data=subset, x="Dev_Stage", y="N_demand", ax=ax, label="N_demand", color='blue', estimator="median", errorbar=("pi", 90))
    sns.lineplot(data=subset, x="Dev_Stage", y="P_demand", ax=ax, label="P_demand", color='green', estimator="median", errorbar=("pi", 90))

    ax.set_xlabel("Development Stage")
    ax.set_ylabel("Nutrient Demand [kg ha-1 day-1]")
    ax.set_title(f"N & P Demand of the basin for year {year} ")
    ax.legend()
    ax.grid()

# Main function to generate side-by-side plots
def plot_side_by_side_seaborn(df, lat, lon, year, StudyArea, crop, output_path):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left Plot (Fixed Lat-Lon, All Years)
    plot_demand_seaborn(axes[0], df, lat, lon)

    # Right Plot (Fixed Year, All Lat-Lon)
    plot_demand_year_fixed_seaborn(axes[1], df, year)

    # Add a title for the whole figure
    plt.suptitle(f"N & P Demand Analysis for {crop} in {StudyArea} river basin", fontsize=14, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit title
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()

StudyAreas = ["Yangtze"] # ["Rhine", "Yangtze", "LaPlata", "Indus"]
crop_types = ["maize","mainrice","secondrice","soybean","winterwheat"]

for StudyArea in StudyAreas:
    for crop in crop_types:
        input_dir = f"/lustre/nobackup/WUR/ESG/zhou111/WOFOST-Nutrient/CaseStudy/{StudyArea}/Output/Daily_his_Yp" # EvaTrans
        input_file = os.path.join(input_dir, f"{StudyArea}_Yp_{crop}_Daily.csv")
        df = pd.read_csv(input_file)
        lat = 30.25
        lon = 107.25
        year = 2000
        output_path = f"/lustre/nobackup/WUR/ESG/zhou111/Plot/CaseStudy_Nutri_Demand/{StudyArea}_{crop}_NutriDemand.png"
        plot_side_by_side_seaborn(df, lat, lon, year, StudyArea, crop, output_path)