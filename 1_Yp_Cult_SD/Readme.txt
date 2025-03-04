The code of this folder is used to:
1_Get_Yp_SD_tsum.py 
    - Analyze the which sowing date + cultivar combinations will give the highest yield for each pixel
    - Store the "Potential_Yield_WOFOST", "Sow_date", "TSUM1", "TSUM2" in a new "mask file" with the name croptype_Yp_his_org.nc

2_Exc_Pixel.py
    - Exclude pixel that has "unreasonable" yield/growing days

    Here: 
    YRB (Yangtze River Basin)
        Main Rice
        Growing days: < 170 days
        Potential yield > 3500 kg/ha, < 14000 kg/ha (the value is set as 14000 kg/ha as it is really hard to find the potential yield larger than that globally)

        Second Rice
        Growing days: < 130 days
        Potential yield > 3500 kg/ha, < 14000 kg/ha (the value is set as 14000 kg/ha as it is really hard to find the potential yield larger than that globally)