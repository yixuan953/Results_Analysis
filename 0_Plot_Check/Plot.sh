#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000

#--------------------Environment, Operations and Job steps-------------
module load python/3.12.0

# 1. Plot the potential yield and harvested area
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/0_Plot_Check/1_Yp_HA.py

# 2. Compare the residue calculated based on wofost simulated results & the residue N input from the literature
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/0_Plot_Check/2_Res_Compare.py

# 3. Plot the irrigation demand
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/0_Plot_Check/3_Irrigation_Demand.py