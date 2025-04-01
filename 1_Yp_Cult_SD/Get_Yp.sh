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

# 1. Extract sowing date + cultivar (tsum 1&2) combinations that gives the highest potential yield
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/1_Yp_Cult_SD/1_Get_Yp_SD_tsum.py

# 2. Exclude unreasonable pixels
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/1_Yp_Cult_SD/2_Exc_Pixel.py

# 3. Copy the output results to the original mask file, in order to guarantee the same spatial ranges for further runs
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/Result_Analysis/1_Yp_Cult_SD/3_Create_New_Mask.py