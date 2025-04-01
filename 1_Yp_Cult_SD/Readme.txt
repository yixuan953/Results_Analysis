The code of this folder is used to:
1_Get_Yp_SD_tsum.py 
    - Analyze the which sowing date + cultivar combinations will give the highest yield for each pixel
    - Store the "Potential_Yield_WOFOST", "Sow_date", "TSUM1", "TSUM2" in a new "mask file" with the name croptype_Yp_his_org.nc

2_Exc_Pixel.py
    - Exclude pixel that has "unreasonable" yield/growing days
    - Get the final crop mask for further simulations

    Here: 
    YRB (Yangtze River Basin)
        Main Rice
        Growing days: < 170 days
        Potential yield > 3500 kg/ha, < 14000 kg/ha (the value is set as 14000 kg/ha as it is really hard to find the potential yield larger than that according to global yield gap atlas)

        Second Rice
        Growing days: < 140 days
        Potential yield > 3500 kg/ha, < 14000 kg/ha (the value is set as 14000 kg/ha as it is really hard to find the potential yield larger than that according to global yield gap atlas)

        Maize
        Growing days: < 140 days
        Potential yield > 3500 kg/ha, < 15000 kg/ha

        Winterwheat
        Growing days: < 140 days
        Potential yield > 3500 kg/ha, < 13000 kg/ha 

        Soybean
        Growing days: < 140 days
        Potential yield > 3500 kg/ha, < 8000 kg/ha