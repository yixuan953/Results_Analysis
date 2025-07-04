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

# 1. Convert wofost daily output from .csv to netcdf
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/2_Irri_Demand/1_Trans_csv2nc_daily.py
conda deactivate