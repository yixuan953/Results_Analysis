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

# Python scripts
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/1_Yp_Cult_SD/1_Get_Yp_SD_tsum.py