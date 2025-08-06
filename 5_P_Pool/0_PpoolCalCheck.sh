#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=/lustre/nobackup/WUR/ESG/zhou111//HPC_Report/output_%j.txt
#SBATCH --error=/lustre/nobackup/WUR/ESG/zhou111//HPC_Report/error_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000

#--------------------Environment, Operations and Job steps-------------
source /home/WUR/zhou111/miniconda3/etc/profile.d/conda.sh
conda activate myenv

# 1. Plot the maps of P pool changes for 4 basins (maize)
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/5_P_Pool/1_P_Pool_Changes.py

# 2. Plot the daily P fluxes v.s. DVS for selected pixels in 4 basins (maize)
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/5_P_Pool/2_P_daily_dynamics.py

# 3. Plot the maps of average annual P flows for 4 basins (maize) 
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/5_P_Pool/3_Prop_Pfluxes.py

# 4. Plot the pillar plot of P fluxes for selected pixels in 4 basins (maize)
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/5_P_Pool/4_PropChanges.py

conda deactivate