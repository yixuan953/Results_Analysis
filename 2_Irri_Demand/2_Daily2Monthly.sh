#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000

#-------------------- Environment, Operations and Job steps -------------
#load modules
module load cdo
module load hdf5

# Path for original input, final output, and processed data that will be deleted.
input_dir="/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/Output/Daily_nc_file"
meteo_input_dir="/lustre/nobackup/WUR/ESG/zhou111/WOFOST-withoutNPLimit/CaseStudy_Meteo"
process_dir="/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Hydro"

# Crop types
StudyAreas=("Rhine") # "Rhine" "Yangtze" "LaPlata" "Indus"
CropTypes=('winterwheat') # 'mainrice' 'secondrice' 'springwheat' 'winterwheat' 'soybean' 'maize'

Cal_Daily_Irri_Demand(){

    for studyarea in "${StudyAreas[@]}"; 
    do  
        meteo_data="${meteo_input_dir}/${studyarea}/${studyarea}_Prec_daily_1981-2019.nc"
        
        for croptype in "${CropTypes[@]}"; 
        do
            wofost_output="${input_dir}/${studyarea}_${croptype}_Yp_daily.nc"
            
            # Cut the meteo data using the mask of wofost_output data
            export HDF5_DISABLE_VERSION_CHECK=1
            cdo remapnn,${wofost_output} ${meteo_data} ${process_dir}/${studyarea}_${croptype}_Prec_daily.nc

            # Calculate the total evapotranspiration
            cdo -expr,"EvaTrans=Transpiration+EvaWater+EvaSoil" ${wofost_output} ${process_dir}/${studyarea}_${croptype}_EvaTrans_daily.nc

            # Calculate the deficit (Evapotranspiration - Precipitation)
            cdo sub ${process_dir}/${studyarea}_${croptype}_EvaTrans_daily.nc ${process_dir}/${studyarea}_${croptype}_Prec_daily.nc ${process_dir}/${studyarea}_${croptype}_Deficit_daily.nc

            # Set negative value to 0 
            cdo setrtoc,-1e3,-0.00001,0 ${process_dir}/${studyarea}_${croptype}_Deficit_daily.nc ${process_dir}/${studyarea}_${croptype}_Deficit_daily_noNeg.nc

        done
    done    
}

Daily_to_Monthly(){
    for studyarea in "${StudyAreas[@]}"; 
    do         
        for croptype in "${CropTypes[@]}"; 
        do
            daily_deficit="${process_dir}/${studyarea}_${croptype}_Deficit_daily_noNeg.nc"
            cdo monsum ${daily_deficit} ${process_dir}/${studyarea}_${croptype}_Deficit_monthly.nc
        done
    done
}



# ------------- List of functions ------------
# 1. Calculate the Daily irrigation demand
Cal_Daily_Irri_Demand

# 2. Aggregate daily irrigation demand to monthly scale
Daily_to_Monthly