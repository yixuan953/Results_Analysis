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

# 1. Get the map to show the average annual surface runoff
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/4_WatBal_Analysis/1_Rice_WatBal.py

# 2. Show the time series of surface runoff and DVS for 3 example points
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/4_WatBal_Analysis/2_Rice_WatBal_TimeSeries.py

conda deactivate