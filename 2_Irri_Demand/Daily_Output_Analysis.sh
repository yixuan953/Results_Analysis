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

# 1. Convert wofost daily output from .csv to netcdf
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/2_Irri_Demand/1_Trans_csv2nc_daily.py