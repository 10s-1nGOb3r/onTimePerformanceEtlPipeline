import pandas as pd
import numpy as np
import os

# Get the folder where otp_calculation.py is actually located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the CSV file correctly
file_path = os.path.join(script_dir, "input", "otp_pandas_try.csv")
file_path2 = os.path.join(script_dir, "input", "delco_data_try.csv")
file_path3 = os.path.join(script_dir, "input", "station_db.csv")
output_folder = os.path.join(script_dir, "output")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Now read it
df = pd.read_csv(file_path, sep=";", dtype={14: str, 17: str, 20: str, 26: str, 13: str, 25: str})

# Check if it exists, if not, create it!
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created missing directory: {output_folder}")

# Start with data cleansing and data formatting
df["DATE"] = pd.to_datetime(df["DATE"], format="%d/%m/%Y", errors="coerce")
df["MONTH_NUMBER"] = df["DATE"].dt.month
df["MONTH_NAME"] = df["DATE"].dt.month_name()
df["YEAR"] = df["DATE"].dt.year
df["ST"] = df["ST"].fillna("0")
df["C1"] = df["C1"].fillna("0")
df["C1"] = df["C1"].astype(str)
df["C1"] = df["C1"].str.split(".").str[0]
df["C2"] = df["C2"].fillna("0")
df["C2"] = df["C2"].astype(str)
df["C2"] = df["C2"].str.split(".").str[0]
df["C3"] = df["C3"].fillna("0")
df["C3"] = df["C3"].astype(str)
df["C3"] = df["C3"].str.split(".").str[0]
df["C4"] = df["C4"].fillna("0")
df["C4"] = df["C4"].astype(str)
df["C4"] = df["C4"].str.split(".").str[0]
df["C1Arr"] = df["C1Arr"].fillna("0")
df["C1Arr"] = df["C1Arr"].astype(str)
df["C1Arr"] = df["C1Arr"].str.split(".").str[0]
df["C2Arr"] = df["C2Arr"].fillna("0")
df["C2Arr"] = df["C2Arr"].astype(str)
df["C2Arr"] = df["C2Arr"].str.split(".").str[0]
df["DLY1"] = df["DLY1"].fillna("00:00:00")
df["DLY1"] = pd.to_timedelta(df["DLY1"].astype(str) + ":00",errors="coerce")
df["DLY1"] = df["DLY1"].fillna(pd.Timedelta(seconds=0))
df["DLY1"] = df["DLY1"] / pd.Timedelta(minutes=1)
df["DLY2"] = df["DLY2"].fillna("00:00:00")
df["DLY2"] = pd.to_timedelta(df["DLY2"].astype(str) + ":00",errors="coerce")
df["DLY2"] = df["DLY2"].fillna(pd.Timedelta(seconds=0))
df["DLY2"] = df["DLY2"] / pd.Timedelta(minutes=1)
df["DLY3"] = df["DLY3"].fillna("0")
df["DLY3"] = pd.to_timedelta(df["DLY3"].astype(str) + ":00", errors="coerce")
df["DLY3"] = df["DLY3"].fillna(pd.Timedelta(seconds=0))
df["DLY3"] = df["DLY3"] / pd.Timedelta(minutes=1)
df["DLY4"] = df["DLY4"].fillna("0")
df["DLY4"] = pd.to_timedelta(df["DLY4"].astype(str) + ":00", errors="coerce")
df["DLY4"] = df["DLY4"].fillna(pd.Timedelta(seconds=0))
df["DLY4"] = df["DLY4"] / pd.Timedelta(minutes=1)
df["DLY1Arr"] = df["DLY1Arr"].fillna("0")
df["DLY1Arr"] = pd.to_timedelta(df["DLY1Arr"].astype(str) + ":00", errors="coerce")
df["DLY1Arr"] = df["DLY1Arr"].fillna(pd.Timedelta(seconds=0))
df["DLY1Arr"] = df["DLY1Arr"] / pd.Timedelta(minutes=1)
df["DLY2Arr"] = df["DLY2Arr"].fillna("0")
df["DLY2Arr"] = pd.to_timedelta(df["DLY2Arr"].astype(str) + ":00", errors="coerce")
df["DLY2Arr"] = df["DLY2Arr"].fillna(pd.Timedelta(seconds=0))
df["DLY2Arr"] = df["DLY2Arr"] / pd.Timedelta(minutes=1)
df["Sub1"] = df["Sub1"].fillna("0")
df["Sub2"] = df["Sub2"].fillna("0")
df["Sub3"] = df["Sub3"].fillna("0")
df["Sub4"] = df["Sub4"].fillna("0")
df["Sub1Arr"] = df["Sub1Arr"].fillna("0")
df["Sub2Arr"] = df["Sub2Arr"].fillna("0")
df["C1"] = np.where(df["Sub1"] != "0", df["C1"] + df["Sub1"], df["C1"])
df["C1"] = df["C1"].astype(str)
df["C2"] = np.where(df["Sub2"] != "0", df["C2"] + df["Sub2"], df["C2"])
df["C2"] = df["C2"].astype(str)
df["C3"] = np.where(df["Sub3"] != "0", df["C3"] + df["Sub3"], df["C3"])
df["C3"] = df["C3"].astype(str)
df["C4"] = np.where(df["Sub4"] != "0", df["C4"] + df["Sub4"], df["C4"])
df["C4"] = df["C4"].astype(str)
df["C1Arr"] = np.where(df["Sub1Arr"] != "0", df["C1Arr"] + df["Sub1Arr"], df["C1Arr"])
df["C1Arr"] = df["C1Arr"].astype(str)
df["C2Arr"] = np.where(df["Sub2Arr"] != "0", df["C2Arr"] + df["Sub2Arr"], df["C2Arr"])
df["C2Arr"] = df["C2Arr"].astype(str)

# Validating for counted flight and delayed flight logic
FValCond = ((df["TYPE"] == "J") | (df["TYPE"] == "G")) & (df["ST"] == "0")
df["FVal"] = np.where(FValCond, "val", "not_count")

df["stationVal"] = np.where(df["FVal"] == "val", df["DEP"], "0")

df["stationValArr"] = np.where(df["FVal"] == "val", df["ARR"], "0")

df["DelTotDep"] = np.where((df["FVal"] == "val") & ((df["DLY1"] + df["DLY2"] + df["DLY3"] + df["DLY4"]) > 15), df["DLY1"] + df["DLY2"] + df["DLY3"] + df["DLY4"], 0)
Dly = df["DelTotDep"] > 15
onTime = df["DelTotDep"] <= 15
df["DelVal"] = np.where((df["FVal"] == "val") & Dly, "late",
                        np.where((df["FVal"] == "val") & onTime, "on_time", "0"))

# Filtering for every delay category by length & delay code assignment logic
df["DelRange"] = np.where(((df["DelTotDep"] > 15) & (df["DelTotDep"] <= 30)) & (df["FVal"] == "val") & (df["DelVal"] == "late"), "00:16 - 00:30", 
                        np.where(((df["DelTotDep"] > 30) & (df["DelTotDep"] < 60)) & (df["FVal"] == "val") & (df["DelVal"] == "late"), "00:31 - 00:59",
                        np.where(((df["DelTotDep"] >= 60) & (df["DelTotDep"] < 120)) & (df["FVal"] == "val") & (df["DelVal"] == "late"), "01:00 - 01:59",
                        np.where(((df["DelTotDep"] >= 120) & (df["DelTotDep"] < 240)) & (df["FVal"] == "val") & (df["DelVal"] == "late"), "02:00 - 03:59",
                        np.where((df["DelTotDep"] > 240) & (df["FVal"] == "val") & (df["DelVal"] == "late"), "> 04:00","0")))))

DlyMax = df[["DLY1", "DLY2", "DLY3", "DLY4"]].max(axis=1)
df["DlyCodeAsgn"] = np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY1"]), df["C1"],
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY2"]), df["C2"],
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY3"]), df["C3"],
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY4"]), df["C4"], 
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY1"]) & (DlyMax == df["DLY2"]), df["C1"], 
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY1"]) & (DlyMax == df["DLY2"]) & (DlyMax == df["DLY3"]), df["C1"],  
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "late") & (DlyMax == df["DLY1"]) & (DlyMax == df["DLY2"]) & (DlyMax == df["DLY3"]) & (DlyMax == df["DLY4"]), df["C1"], 
                            np.where((df["FVal"] == "val") & (df["DelVal"] == "on_time"), 3, 0))))))))

# Validating delay arrival flight logic
df["DelTotArr"] = np.where((df["FVal"] == "val") & ((df["DLY1Arr"] + df["DLY2Arr"]) > 15), df["DLY1Arr"] + df["DLY2Arr"], 0)
DlyArr = df["DelTotArr"] > 15
onTimeArr = df["DelTotArr"] <= 15
df["DelValArr"] = np.where((df["FVal"] == "val") & DlyArr, "late",
                        np.where((df["FVal"] == "val") & onTimeArr, "on_time", "0"))

# Filtering for every delay category arrival by length & delay code assignment logic
df["DelRangeArr"] = np.where(((df["DelTotArr"] > 15) & (df["DelTotArr"] <= 30)) & (df["FVal"] == "val") & (df["DelValArr"] == "late"), "00:16 - 00:30", 
                        np.where(((df["DelTotArr"] > 30) & (df["DelTotArr"] < 60)) & (df["FVal"] == "val") & (df["DelValArr"] == "late"), "00:31 - 00:59",
                        np.where(((df["DelTotArr"] >= 60) & (df["DelTotArr"] < 120)) & (df["FVal"] == "val") & (df["DelValArr"] == "late"), "01:00 - 01:59",
                        np.where(((df["DelTotArr"] >= 120) & (df["DelTotArr"] < 240)) & (df["FVal"] == "val") & (df["DelValArr"] == "late"), "02:00 - 03:59",
                        np.where((df["DelTotArr"] > 240) & (df["FVal"] == "val") & (df["DelValArr"] == "late"), "> 04:00","0")))))

DlyMaxArr = df[["DLY1Arr", "DLY2Arr"]].max(axis=1)
df["DlyCodeAsgnArr"] = np.where((df["FVal"] == "val") & (df["DelValArr"] == "late") & (DlyMaxArr == df["DLY1Arr"]), df["C1Arr"],
                            np.where((df["FVal"] == "val") & (df["DelValArr"] == "late") & (DlyMaxArr == df["DLY2Arr"]), df["C2Arr"],
                            np.where((df["FVal"] == "val") & (df["DelValArr"] == "late") & (DlyMaxArr == df["DLY1Arr"]) & (DlyMaxArr == df["DLY2Arr"]), df["C1Arr"], 
                            np.where((df["FVal"] == "val") & (df["DelValArr"] == "on_time"), 3, 0))))

dc = pd.read_csv(file_path2, sep=";")
st = pd.read_csv(file_path3, sep=";")

# Converting fields that will be used to merge table
df["DlyCodeAsgn"] = df["DlyCodeAsgn"].astype(str)
df["DlyCodeAsgnArr"] = df["DlyCodeAsgnArr"].astype(str)
df["C1"] = df["C1"].astype(str)
df["C2"] = df["C2"].astype(str)
df["C3"] = df["C3"].astype(str)
df["C4"] = df["C4"].astype(str)
df["C1Arr"] = df["C1Arr"].astype(str)
df["C2Arr"] = df["C2Arr"].astype(str)
df["stationVal"] = df["stationVal"].astype(str)
df["stationValArr"] = df["stationValArr"].astype(str)

# Reading the input file to be merged into Daily Flight Schedule table
dc_small = dc[["DlyCodeAsgn", "DlyCat", "DlyCat2"]].astype(str)
st_small = st[["STATION","ICAO","CLASS","TOWN","ZONE"]].astype(str)

# Merge the table for Departure OTP Fields
df2 = pd.merge(df, dc_small, how="left", on="DlyCodeAsgn", suffixes=("", "_main")).drop(columns="DlyCodeAsgn_main", errors='ignore')
df2 = pd.merge(df2, st_small, how="left", left_on="stationVal", right_on="STATION", suffixes=("","_stn")).drop(columns="stn_main", errors='ignore')
df2 = pd.merge(df2, dc_small, how="left", left_on="C1", right_on="DlyCodeAsgn", suffixes=("", "_c1")).drop(columns="DlyCodeAsgn_c1", errors='ignore')
df2 = pd.merge(df2, dc_small, how="left", left_on="C2", right_on="DlyCodeAsgn", suffixes=("", "_c2")).drop(columns="DlyCodeAsgn_c2", errors='ignore')
df2 = pd.merge(df2, dc_small, how="left", left_on="C3", right_on="DlyCodeAsgn", suffixes=("", "_c3")).drop(columns="DlyCodeAsgn_c3", errors='ignore')
df2 = pd.merge(df2, dc_small, how="left", left_on="C4", right_on="DlyCodeAsgn", suffixes=("", "_c4")).drop(columns="DlyCodeAsgn_c4", errors='ignore')

df2 = df2.rename(columns={
    "DlyCat": "Main_Cat1",
    "DlyCat2": "Main_Cat2",
    "DlyCat_c1": "C1_Cat1",
    "DlyCat2_c1": "C1_Cat2",
    "DlyCat_c2": "C2_Cat1",
    "DlyCat2_c2": "C2_Cat2",
    "DlyCat_c3": "C3_Cat1",
    "DlyCat2_c3": "C3_Cat2",
    "DlyCat_c4": "C4_Cat1",
    "DlyCat2_c4": "C4_Cat2",
    "StationCnt" : "StationFlt",
    "StationCode1": "StationIcao",
    "StationCode2": "StationClass"
})

# Merge the table for Arrival OTP Fields
df2 = pd.merge(df2, dc_small, how="left", left_on="DlyCodeAsgnArr", right_on="DlyCodeAsgn", suffixes=("", "_mainArr")).drop(columns="DlyCodeAsgn_mainArr", errors='ignore')
df2 = pd.merge(df2, st_small, how="left", left_on="stationValArr", right_on="STATION", suffixes=("","_stnArr")).drop(columns="stn_mainArr", errors='ignore')
df2 = pd.merge(df2, dc_small, how="left", left_on="C1Arr", right_on="DlyCodeAsgn", suffixes=("", "_c1Arr")).drop(columns="DlyCodeAsgn_c1Arr", errors='ignore')
df2 = pd.merge(df2, dc_small, how="left", left_on="C2Arr", right_on="DlyCodeAsgn", suffixes=("", "_c2Arr")).drop(columns="DlyCodeAsgn_c2Arr", errors='ignore')

df2 = df2.rename(columns={
    "DlyCat": "Main_CatArr1",
    "DlyCat2": "Main_CatArr2",   
    "DlyCat_c1Arr": "C1Arr_Cat1",   
    "DlyCat2_c1Arr": "C1Arr_Cat2",   
    "DlyCat_c2Arr": "C2Arr_Cat1",   
    "DlyCat2_c2Arr": "C2Arr_Cat2"
})

# Composing cause of delay fields that will be used for percentage in aggregate tables
flt_valid = df2["FVal"] == "val"
dly_valid = df2["DelVal"] == "late"
dlyArr_valid = df2["DelValArr"] == "late"

stnHndl1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "STATION HANDLING"), df2["DLY1"], 0)
stnHndl2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "STATION HANDLING"), df2["DLY2"], 0)
stnHndl3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "STATION HANDLING"), df2["DLY3"], 0)
stnHndl4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "STATION HANDLING"), df2["DLY4"], 0)
df2["StnHndlDelay"] = stnHndl1 + stnHndl2 + stnHndl3 + stnHndl4

damAc1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "DAMAGE TO AIRCRAFT"), df2["DLY1"], 0)
damAc2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "DAMAGE TO AIRCRAFT"), df2["DLY2"], 0)
damAc3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "DAMAGE TO AIRCRAFT"), df2["DLY3"], 0)
damAc4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "DAMAGE TO AIRCRAFT"), df2["DLY4"], 0)
df2["DamAcDelay"] = damAc1 + damAc2 + damAc3 + damAc4

tech1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "TECHNICAL"), df2["DLY1"], 0)
tech2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "TECHNICAL"), df2["DLY2"], 0)
tech3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "TECHNICAL"), df2["DLY3"], 0)
tech4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "TECHNICAL"), df2["DLY4"], 0)
df2["TechDelay"] = tech1 + tech2 + tech3 + tech4

syst1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "SYSTEM"), df2["DLY1"], 0)
syst2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "SYSTEM"), df2["DLY2"], 0)
syst3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "SYSTEM"), df2["DLY3"], 0)
syst4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "SYSTEM"), df2["DLY4"], 0)
df2["SystDelay"] = syst1 + syst2 + syst3 + syst4

flops1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "FLIGHT OPERATIONS & CREW"), df2["DLY1"], 0)
flops2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "FLIGHT OPERATIONS & CREW"), df2["DLY2"], 0)
flops3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "FLIGHT OPERATIONS & CREW"), df2["DLY3"], 0)
flops4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "FLIGHT OPERATIONS & CREW"), df2["DLY4"], 0)
df2["FlopsDelay"] = flops1 + flops2 + flops3 + flops4

weather1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "WEATHER"), df2["DLY1"], 0)
weather2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "WEATHER"), df2["DLY2"], 0)
weather3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "WEATHER"), df2["DLY3"], 0)
weather4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "WEATHER"), df2["DLY4"], 0)
df2["WeatherDelay"] = weather1 + weather2 + weather3 + weather4

airport1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "AIRPORT FACILITIES"), df2["DLY1"], 0)
airport2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "AIRPORT FACILITIES"), df2["DLY2"], 0)
airport3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "AIRPORT FACILITIES"), df2["DLY3"], 0)
airport4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "AIRPORT FACILITIES"), df2["DLY4"], 0)
df2["AirportDelay"] = airport1 + airport2 + airport3 + airport4

misc1 = np.where(flt_valid & dly_valid & (df2["C1_Cat1"] == "MISCELLANEOUS"), df2["DLY1"], 0)
misc2 = np.where(flt_valid & dly_valid & (df2["C2_Cat1"] == "MISCELLANEOUS"), df2["DLY2"], 0)
misc3 = np.where(flt_valid & dly_valid & (df2["C3_Cat1"] == "MISCELLANEOUS"), df2["DLY3"], 0)
misc4 = np.where(flt_valid & dly_valid & (df2["C4_Cat1"] == "MISCELLANEOUS"), df2["DLY4"], 0)
df2["MiscDelay"] = misc1 + misc2 + misc3 + misc4

control1 = np.where(flt_valid & dly_valid & (df2["C1_Cat2"] == "CONTROLLABLE"), df2["DLY1"], 0)
control2 = np.where(flt_valid & dly_valid & (df2["C2_Cat2"] == "CONTROLLABLE"), df2["DLY2"], 0)
control3 = np.where(flt_valid & dly_valid & (df2["C3_Cat2"] == "CONTROLLABLE"), df2["DLY3"], 0)
control4 = np.where(flt_valid & dly_valid & (df2["C4_Cat2"] == "CONTROLLABLE"), df2["DLY4"], 0)
df2["ControlDelay"] = control1 + control2 + control3 + control4

uncontrol1 = np.where(flt_valid & dly_valid & (df2["C1_Cat2"] == "UNCONTROLLABLE"), df2["DLY1"], 0)
uncontrol2 = np.where(flt_valid & dly_valid & (df2["C2_Cat2"] == "UNCONTROLLABLE"), df2["DLY2"], 0)
uncontrol3 = np.where(flt_valid & dly_valid & (df2["C3_Cat2"] == "UNCONTROLLABLE"), df2["DLY3"], 0)
uncontrol4 = np.where(flt_valid & dly_valid & (df2["C4_Cat2"] == "UNCONTROLLABLE"), df2["DLY4"], 0)
df2["UncontrolDelay"] = uncontrol1 + uncontrol2 + uncontrol3 + uncontrol4

stnHndlArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "STATION HANDLING"), df2["DLY1Arr"], 0)
stnHndlArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "STATION HANDLING"), df2["DLY2Arr"], 0)
df2["StnHndlDelayArr"] = stnHndlArr1 + stnHndlArr2

damAcArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "DAMAGE TO AIRCRAFT"), df2["DLY1Arr"], 0)
damAcArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "DAMAGE TO AIRCRAFT"), df2["DLY2Arr"], 0)
df2["damAcArr"] = damAcArr1 + damAcArr2

techArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "TECHNICAL"), df2["DLY1Arr"], 0)
techArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "TECHNICAL"), df2["DLY2Arr"], 0)
df2["techArr"] = techArr1 + techArr2

systArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "SYSTEM"), df2["DLY1Arr"], 0)
systArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "SYSTEM"), df2["DLY2Arr"], 0)
df2["systArr"] = systArr1 + systArr2

flopsArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "FLIGHT OPERATIONS & CREW"), df2["DLY1Arr"], 0)
flopsArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "FLIGHT OPERATIONS & CREW"), df2["DLY2Arr"], 0)
df2["flopsArr"] = flopsArr1 + flopsArr2

weatherArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "WEATHER"), df2["DLY1Arr"], 0)
weatherArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "WEATHER"), df2["DLY2Arr"], 0)
df2["weatherArr"] = weatherArr1 + weatherArr2

airportArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "AIRPORT FACILITIES"), df2["DLY1Arr"], 0)
airportArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "AIRPORT FACILITIES"), df2["DLY2Arr"], 0)
df2["airportArr"] = airportArr1 + airportArr2

miscArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat1"] == "MISCELLANEOUS"), df2["DLY1Arr"], 0)
miscArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat1"] == "MISCELLANEOUS"), df2["DLY2Arr"], 0)
df2["miscArr"] = miscArr1 + miscArr2

controlArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat2"] == "CONTROLLABLE"), df2["DLY1Arr"], 0)
controlArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat2"] == "CONTROLLABLE"), df2["DLY2Arr"], 0)
df2["controlArr"] = controlArr1 + controlArr2

uncontrolArr1 = np.where(flt_valid & dlyArr_valid & (df2["C1Arr_Cat2"] == "UNCONTROLLABLE"), df2["DLY1Arr"], 0)
uncontrolArr2 = np.where(flt_valid & dlyArr_valid & (df2["C2Arr_Cat2"] == "UNCONTROLLABLE"), df2["DLY2Arr"], 0)
df2["uncontrolArr"] = uncontrolArr1 + uncontrolArr2

df2["station_town"] = np.where(flt_valid, df2["STATION"] + " - " + df2["TOWN"],0)
df2["station_townArr"] = np.where(flt_valid, df2["STATION_stnArr"] + " - " + df2["TOWN_stnArr"],0)

# Aggregation for the composed table
otpPerDate = df.groupby(["DATE"]).agg(
    flightPerDate = ("FVal", lambda x: (x == "val").sum()),
    onTimePerDate = ("DelVal", lambda x: (x == "on_time").sum()),
    latePerDate = ("DelVal", lambda x: (x == "late").sum())
).reset_index()

otpPerDate["onTimePerDate"] = otpPerDate["onTimePerDate"].astype(int)
otpPerDate["flightPerDate"] = otpPerDate["flightPerDate"].astype(int)
otpPerDate["OTP_Percentage"] = round((otpPerDate["onTimePerDate"] / otpPerDate["flightPerDate"]) * 100 ,2)

otpArrPerDate = df.groupby(["DATE"]).agg(
    flightPerDate = ("FVal", lambda x: (x == "val").sum()),
    onTimePerDate = ("DelValArr", lambda x: (x == "on_time").sum()),
    latePerDate = ("DelValArr", lambda x: (x == "late").sum())
).reset_index()

otpArrPerDate["onTimePerDate"] = otpArrPerDate["onTimePerDate"].astype(int)
otpArrPerDate["flightPerDate"] = otpArrPerDate["flightPerDate"].astype(int)
otpArrPerDate["OTP_PercentageArr"] = round((otpArrPerDate["onTimePerDate"] / otpArrPerDate["flightPerDate"]) * 100 ,2)

otpPerMonth = df.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME"]).agg(
    flightPerMonth = ("FVal", lambda x: (x == "val").sum()),
    onTimePerMonth = ("DelVal", lambda x: (x == "on_time").sum()),
    latePerMonth = ("DelVal", lambda x: (x == "late").sum())
).reset_index()

otpPerMonth["onTimePerMonth"] = otpPerMonth["onTimePerMonth"].astype(int)
otpPerMonth["flightPerMonth"] = otpPerMonth["flightPerMonth"].astype(int)
otpPerMonth["OTP_Percentage"] = round((otpPerMonth["onTimePerMonth"] / otpPerMonth["flightPerMonth"]) * 100 ,2)

otpArrPerMonth = df.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME"]).agg(
    flightPerMonth = ("FVal", lambda x: (x == "val").sum()),
    onTimePerMonth = ("DelValArr", lambda x: (x == "on_time").sum()),
    latePerMonth = ("DelValArr", lambda x: (x == "late").sum())
).reset_index()

otpArrPerMonth["onTimePerMonth"] = otpArrPerMonth["onTimePerMonth"].astype(int)
otpArrPerMonth["flightPerMonth"] = otpArrPerMonth["flightPerMonth"].astype(int)
otpArrPerMonth["OTP_Percentage"] = round((otpArrPerMonth["onTimePerMonth"] / otpArrPerMonth["flightPerMonth"]) * 100 ,2)

delCatNum = df2.groupby("DATE").agg(
    stnhndlCount = ("Main_Cat1", lambda x: (x == "STATION HANDLING").sum()),
    damAcCount = ("Main_Cat1", lambda x: (x == "DAMAGE TO AIRCRAFT").sum()),
    techCount = ("Main_Cat1", lambda x: (x == "TECHNICAL").sum()),
    systCount = ("Main_Cat1", lambda x: (x == "SYSTEM").sum()),
    flopsCount = ("Main_Cat1", lambda x: (x == "FLIGHT OPERATIONS & CREW").sum()),
    weatherCount = ("Main_Cat1", lambda x: (x == "WEATHER").sum()),
    airportCount = ("Main_Cat1", lambda x: (x == "AIRPORT FACILITIES").sum()),
    miscCount = ("Main_Cat1", lambda x: (x == "MISCELLANEOUS").sum()),
    controlCount = ("Main_Cat2", lambda x: (x == "CONTROLLABLE").sum()),
    uncontrolCount = ("Main_Cat2", lambda x: (x == "UNCONTROLLABLE").sum()),
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delayedFlights = ("DelVal", lambda x: (x == "late").sum()),   
    delayTotal = ("DelTotDep", "sum"),
    stnHndlTotal = ("StnHndlDelay", "sum"),
    damAcTotal = ("DamAcDelay", "sum"),
    techTotal = ("TechDelay", "sum"),
    systTotal = ("SystDelay", "sum"),
    flopsTotal = ("FlopsDelay", "sum"),
    weatherTotal = ("WeatherDelay", "sum"),
    airportTotal = ("AirportDelay", "sum"),
    miscTotal = ("MiscDelay", "sum"),
    ctrlTotal = ("ControlDelay", "sum"),
    unctrlTotal = ("UncontrolDelay", "sum")
).reset_index()

delCatNum["stnHandlPerc"] = round((delCatNum["stnHndlTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["damAcPerc"] = round((delCatNum["damAcTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["techPerc"] = round((delCatNum["techTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["systPerc"] = round((delCatNum["systTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["flopsPerc"] = round((delCatNum["flopsTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["weatherPerc"] = round((delCatNum["weatherTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["airportPerc"] = round((delCatNum["airportTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["miscPerc"] = round((delCatNum["miscTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["ctrlPerc"] = round((delCatNum["ctrlTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)
delCatNum["unctrlPerc"] = round((delCatNum["unctrlTotal"] / delCatNum["delayTotal"]) * (delCatNum["delayedFlights"] / delCatNum["fltTotal"]) * 100, 2)

delCatNum2 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME"]).agg(
    stnhndlCount = ("Main_Cat1", lambda x: (x == "STATION HANDLING").sum()),
    damAcCount = ("Main_Cat1", lambda x: (x == "DAMAGE TO AIRCRAFT").sum()),
    techCount = ("Main_Cat1", lambda x: (x == "TECHNICAL").sum()),
    systCount = ("Main_Cat1", lambda x: (x == "SYSTEM").sum()),
    flopsCount = ("Main_Cat1", lambda x: (x == "FLIGHT OPERATIONS & CREW").sum()),
    weatherCount = ("Main_Cat1", lambda x: (x == "WEATHER").sum()),
    airportCount = ("Main_Cat1", lambda x: (x == "AIRPORT FACILITIES").sum()),
    miscCount = ("Main_Cat1", lambda x: (x == "MISCELLANEOUS").sum()),
    controlCount = ("Main_Cat2", lambda x: (x == "CONTROLLABLE").sum()),
    uncontrolCount = ("Main_Cat2", lambda x: (x == "UNCONTROLLABLE").sum()),
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delayedFlights = ("DelVal", lambda x: (x == "late").sum()),   
    delayTotal = ("DelTotDep", "sum"),
    stnHndlTotal = ("StnHndlDelay", "sum"),
    damAcTotal = ("DamAcDelay", "sum"),
    techTotal = ("TechDelay", "sum"),
    systTotal = ("SystDelay", "sum"),
    flopsTotal = ("FlopsDelay", "sum"),
    weatherTotal = ("WeatherDelay", "sum"),
    airportTotal = ("AirportDelay", "sum"),
    miscTotal = ("MiscDelay", "sum"),
    ctrlTotal = ("ControlDelay", "sum"),
    unctrlTotal = ("UncontrolDelay", "sum")
).reset_index()

delCatNum2["stnHandlPerc"] = round((delCatNum2["stnHndlTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["damAcPerc"] = round((delCatNum2["damAcTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["techPerc"] = round((delCatNum2["techTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["systPerc"] = round((delCatNum2["systTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["flopsPerc"] = round((delCatNum2["flopsTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["weatherPerc"] = round((delCatNum2["weatherTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["airportPerc"] = round((delCatNum2["airportTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["miscPerc"] = round((delCatNum2["miscTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["ctrlPerc"] = round((delCatNum2["ctrlTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)
delCatNum2["unctrlPerc"] = round((delCatNum2["unctrlTotal"] / delCatNum2["delayTotal"]) * (delCatNum2["delayedFlights"] / delCatNum2["fltTotal"]) * 100, 2)

delCatNum14 = df2.groupby(["YEAR"]).agg(
    stnhndlCount = ("Main_Cat1", lambda x: (x == "STATION HANDLING").sum()),
    damAcCount = ("Main_Cat1", lambda x: (x == "DAMAGE TO AIRCRAFT").sum()),
    techCount = ("Main_Cat1", lambda x: (x == "TECHNICAL").sum()),
    systCount = ("Main_Cat1", lambda x: (x == "SYSTEM").sum()),
    flopsCount = ("Main_Cat1", lambda x: (x == "FLIGHT OPERATIONS & CREW").sum()),
    weatherCount = ("Main_Cat1", lambda x: (x == "WEATHER").sum()),
    airportCount = ("Main_Cat1", lambda x: (x == "AIRPORT FACILITIES").sum()),
    miscCount = ("Main_Cat1", lambda x: (x == "MISCELLANEOUS").sum()),
    controlCount = ("Main_Cat2", lambda x: (x == "CONTROLLABLE").sum()),
    uncontrolCount = ("Main_Cat2", lambda x: (x == "UNCONTROLLABLE").sum()),
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delayedFlights = ("DelVal", lambda x: (x == "late").sum()),   
    delayTotal = ("DelTotDep", "sum"),
    stnHndlTotal = ("StnHndlDelay", "sum"),
    damAcTotal = ("DamAcDelay", "sum"),
    techTotal = ("TechDelay", "sum"),
    systTotal = ("SystDelay", "sum"),
    flopsTotal = ("FlopsDelay", "sum"),
    weatherTotal = ("WeatherDelay", "sum"),
    airportTotal = ("AirportDelay", "sum"),
    miscTotal = ("MiscDelay", "sum"),
    ctrlTotal = ("ControlDelay", "sum"),
    unctrlTotal = ("UncontrolDelay", "sum")
).reset_index()

delCatNum14["stnHandlPerc"] = round((delCatNum14["stnHndlTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["damAcPerc"] = round((delCatNum14["damAcTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["techPerc"] = round((delCatNum14["techTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["systPerc"] = round((delCatNum14["systTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["flopsPerc"] = round((delCatNum14["flopsTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["weatherPerc"] = round((delCatNum14["weatherTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["airportPerc"] = round((delCatNum14["airportTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["miscPerc"] = round((delCatNum14["miscTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["ctrlPerc"] = round((delCatNum14["ctrlTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)
delCatNum14["unctrlPerc"] = round((delCatNum14["unctrlTotal"] / delCatNum14["delayTotal"]) * (delCatNum14["delayedFlights"] / delCatNum14["fltTotal"]) * 100, 2)

delCatNum3 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME","CLASS","ICAO","station_town"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delRange1630 = ("DelRange", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRange", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRange", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRange", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRange", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum3["1630perc"] = round((delCatNum3["delRange1630"] / delCatNum3["fltTotal"]) * 100, 2)
delCatNum3["3159perc"] = round((delCatNum3["delRange3159"] / delCatNum3["fltTotal"]) * 100, 2)
delCatNum3["0100perc"] = round((delCatNum3["delRange0100"] / delCatNum3["fltTotal"]) * 100, 2)
delCatNum3["0200perc"] = round((delCatNum3["delRange0200"] / delCatNum3["fltTotal"]) * 100, 2)
delCatNum3["0400perc"] = round((delCatNum3["delRange0400"] / delCatNum3["fltTotal"]) * 100, 2)
delCatNum3["otp"] = round(100 - delCatNum3["1630perc"] - delCatNum3["3159perc"] - delCatNum3 ["0100perc"] - delCatNum3["0200perc"] - delCatNum3["0400perc"], 2)

delCatNum4 = df2.groupby(["DATE","CLASS","ICAO","station_town"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delRange1630 = ("DelRange", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRange", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRange", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRange", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRange", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum4["delRange1630Perc"] = round((delCatNum4["delRange1630"] / delCatNum4["fltTotal"]) * 100, 2)
delCatNum4["delRange3159Perc"] = round((delCatNum4["delRange3159"] / delCatNum4["fltTotal"]) * 100, 2)
delCatNum4["delRange0100Perc"] = round((delCatNum4["delRange0100"] / delCatNum4["fltTotal"]) * 100, 2)
delCatNum4["delRange0200Perc"] = round((delCatNum4["delRange0200"] / delCatNum4["fltTotal"]) * 100, 2)
delCatNum4["delRange0400Perc"] = round((delCatNum4["delRange0400"] / delCatNum4["fltTotal"]) * 100, 2)
delCatNum4["otp"] = round(100 - (delCatNum4["delRange1630Perc"] + delCatNum4["delRange3159Perc"] + delCatNum4["delRange0100Perc"] + delCatNum4["delRange0200Perc"] + delCatNum4["delRange0400Perc"]), 2)

delCatNum5 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME","CLASS"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delRange1630 = ("DelRange", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRange", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRange", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRange", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRange", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum5["delRange1630Perc"] = round((delCatNum5["delRange1630"] / delCatNum5["fltTotal"]) * 100, 2)
delCatNum5["delRange3159Perc"] = round((delCatNum5["delRange3159"] / delCatNum5["fltTotal"]) * 100, 2)
delCatNum5["delRange0100Perc"] = round((delCatNum5["delRange0100"] / delCatNum5["fltTotal"]) * 100, 2)
delCatNum5["delRange0200Perc"] = round((delCatNum5["delRange0200"] / delCatNum5["fltTotal"]) * 100, 2)
delCatNum5["delRange0400Perc"] = round((delCatNum5["delRange0400"] / delCatNum5["fltTotal"]) * 100, 2)
delCatNum5["otp"] = round(100 - (delCatNum5["delRange1630Perc"] + delCatNum5["delRange3159Perc"] + delCatNum5["delRange0100Perc"] + delCatNum5["delRange0200Perc"] + delCatNum5["delRange0400Perc"]), 2)

delCatNum6 = df2.groupby(["DATE","CLASS"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delRange1630 = ("DelRange", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRange", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRange", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRange", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRange", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum6["delRange1630Perc"] = round((delCatNum6["delRange1630"] / delCatNum6["fltTotal"]) * 100, 2)
delCatNum6["delRange3159Perc"] = round((delCatNum6["delRange3159"] / delCatNum6["fltTotal"]) * 100, 2)
delCatNum6["delRange0100Perc"] = round((delCatNum6["delRange0100"] / delCatNum6["fltTotal"]) * 100, 2)
delCatNum6["delRange0200Perc"] = round((delCatNum6["delRange0200"] / delCatNum6["fltTotal"]) * 100, 2)
delCatNum6["delRange0400Perc"] = round((delCatNum6["delRange0400"] / delCatNum6["fltTotal"]) * 100, 2)
delCatNum6["otp"] = round(100 - (delCatNum6["delRange1630Perc"] + delCatNum6["delRange3159Perc"] + delCatNum6["delRange0100Perc"] + delCatNum6["delRange0200Perc"] + delCatNum6["delRange0400Perc"]), 2)

delCatNum7 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME","Main_Cat1"]).agg(
    delRange1630 = ("DelRange", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRange", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRange", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRange", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRange", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum8 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum())
).reset_index()

delCatNum9 = pd.merge(delCatNum7, delCatNum8, how="left", on=["YEAR","MONTH_NUMBER","MONTH_NAME"])

delCatNum9["delRange1630Perc"] = round((delCatNum9["delRange1630"] / delCatNum9["fltTotal"]) * 100, 2)
delCatNum9["delRange3159Perc"] = round((delCatNum9["delRange3159"] / delCatNum9["fltTotal"]) * 100, 2)
delCatNum9["delRange0100Perc"] = round((delCatNum9["delRange0100"] / delCatNum9["fltTotal"]) * 100, 2)
delCatNum9["delRange0200Perc"] = round((delCatNum9["delRange0200"] / delCatNum9["fltTotal"]) * 100, 2)
delCatNum9["delRange0400Perc"] = round((delCatNum9["delRange0400"] / delCatNum9["fltTotal"]) * 100, 2)

delCatNum10 = df2.groupby("DATE").agg(
    stnhndlCount = ("Main_CatArr1", lambda x: (x == "STATION HANDLING").sum()),
    damAcCount = ("Main_CatArr1", lambda x: (x == "DAMAGE TO AIRCRAFT").sum()),
    techCount = ("Main_CatArr1", lambda x: (x == "TECHNICAL").sum()),
    systCount = ("Main_CatArr1", lambda x: (x == "SYSTEM").sum()),
    flopsCount = ("Main_CatArr1", lambda x: (x == "FLIGHT OPERATIONS & CREW").sum()),
    weatherCount = ("Main_CatArr1", lambda x: (x == "WEATHER").sum()),
    airportCount = ("Main_CatArr1", lambda x: (x == "AIRPORT FACILITIES").sum()),
    miscCount = ("Main_CatArr1", lambda x: (x == "MISCELLANEOUS").sum()),
    controlCount = ("Main_CatArr2", lambda x: (x == "CONTROLLABLE").sum()),
    uncontrolCount = ("Main_CatArr2", lambda x: (x == "UNCONTROLLABLE").sum()),
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delayedFlights = ("DelValArr", lambda x: (x == "late").sum()),   
    delayTotal = ("DelTotArr", "sum"),
    stnHndlTotal = ("StnHndlDelayArr", "sum"),
    damAcTotal = ("damAcArr", "sum"),
    techTotal = ("techArr", "sum"),
    systTotal = ("systArr", "sum"),
    flopsTotal = ("flopsArr", "sum"),
    weatherTotal = ("weatherArr", "sum"),
    airportTotal = ("airportArr", "sum"),
    miscTotal = ("miscArr", "sum"),
    ctrlTotal = ("controlArr", "sum"),
    unctrlTotal = ("uncontrolArr", "sum")
).reset_index()

delCatNum10["stnHandlPerc"] = round((delCatNum10["stnHndlTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["damAcPerc"] = round((delCatNum10["damAcTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["techPerc"] = round((delCatNum10["techTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["systPerc"] = round((delCatNum10["systTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["flopsPerc"] = round((delCatNum10["flopsTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["weatherPerc"] = round((delCatNum10["weatherTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["airportPerc"] = round((delCatNum10["airportTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["miscPerc"] = round((delCatNum10["miscTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["ctrlPerc"] = round((delCatNum10["ctrlTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)
delCatNum10["unctrlPerc"] = round((delCatNum10["unctrlTotal"] / delCatNum10["delayTotal"]) * (delCatNum10["delayedFlights"] / delCatNum10["fltTotal"]) * 100, 2)

delCatNum11 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME"]).agg(
    stnhndlCount = ("Main_CatArr1", lambda x: (x == "STATION HANDLING").sum()),
    damAcCount = ("Main_CatArr1", lambda x: (x == "DAMAGE TO AIRCRAFT").sum()),
    techCount = ("Main_CatArr1", lambda x: (x == "TECHNICAL").sum()),
    systCount = ("Main_CatArr1", lambda x: (x == "SYSTEM").sum()),
    flopsCount = ("Main_CatArr1", lambda x: (x == "FLIGHT OPERATIONS & CREW").sum()),
    weatherCount = ("Main_CatArr1", lambda x: (x == "WEATHER").sum()),
    airportCount = ("Main_CatArr1", lambda x: (x == "AIRPORT FACILITIES").sum()),
    miscCount = ("Main_CatArr1", lambda x: (x == "MISCELLANEOUS").sum()),
    controlCount = ("Main_CatArr2", lambda x: (x == "CONTROLLABLE").sum()),
    uncontrolCount = ("Main_CatArr2", lambda x: (x == "UNCONTROLLABLE").sum()),
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delayedFlights = ("DelValArr", lambda x: (x == "late").sum()),   
    delayTotal = ("DelTotArr", "sum"),
    stnHndlTotal = ("StnHndlDelayArr", "sum"),
    damAcTotal = ("damAcArr", "sum"),
    techTotal = ("techArr", "sum"),
    systTotal = ("systArr", "sum"),
    flopsTotal = ("flopsArr", "sum"),
    weatherTotal = ("weatherArr", "sum"),
    airportTotal = ("airportArr", "sum"),
    miscTotal = ("miscArr", "sum"),
    ctrlTotal = ("controlArr", "sum"),
    unctrlTotal = ("uncontrolArr", "sum")
).reset_index()

delCatNum11["stnHandlPerc"] = round((delCatNum11["stnHndlTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["damAcPerc"] = round((delCatNum11["damAcTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["techPerc"] = round((delCatNum11["techTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["systPerc"] = round((delCatNum11["systTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["flopsPerc"] = round((delCatNum11["flopsTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["weatherPerc"] = round((delCatNum11["weatherTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["airportPerc"] = round((delCatNum11["airportTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["miscPerc"] = round((delCatNum11["miscTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["ctrlPerc"] = round((delCatNum11["ctrlTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)
delCatNum11["unctrlPerc"] = round((delCatNum11["unctrlTotal"] / delCatNum11["delayTotal"]) * (delCatNum11["delayedFlights"] / delCatNum11["fltTotal"]) * 100, 2)

delCatNum12 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME","CLASS_stnArr","ICAO_stnArr","station_townArr"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delRange1630 = ("DelRangeArr", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRangeArr", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRangeArr", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRangeArr", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRangeArr", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum12["1630perc"] = round((delCatNum12["delRange1630"] / delCatNum12["fltTotal"]) * 100, 2)
delCatNum12["3159perc"] = round((delCatNum12["delRange3159"] / delCatNum12["fltTotal"]) * 100, 2)
delCatNum12["0100perc"] = round((delCatNum12["delRange0100"] / delCatNum12["fltTotal"]) * 100, 2)
delCatNum12["0200perc"] = round((delCatNum12["delRange0200"] / delCatNum12["fltTotal"]) * 100, 2)
delCatNum12["0400perc"] = round((delCatNum12["delRange0400"] / delCatNum12["fltTotal"]) * 100, 2)
delCatNum12["otp"] = round(100 - delCatNum12["1630perc"] - delCatNum12["3159perc"] - delCatNum12["0100perc"] - delCatNum12["0200perc"] - delCatNum12["0400perc"], 2)

delCatNum13 = df2.groupby(["DATE","CLASS_stnArr","ICAO_stnArr","station_townArr"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    delRange1630 = ("DelRange", lambda x: (x == "00:16 - 00:30").sum()),
    delRange3159 = ("DelRange", lambda x: (x == "00:31 - 00:59").sum()),
    delRange0100 = ("DelRange", lambda x: (x == "01:00 - 01:59").sum()),
    delRange0200 = ("DelRange", lambda x: (x == "02:00 - 03:59").sum()),
    delRange0400 = ("DelRange", lambda x: (x == "> 04:00").sum())
).reset_index()

delCatNum13["delRange1630Perc"] = round((delCatNum13["delRange1630"] / delCatNum13["fltTotal"]) * 100, 2)
delCatNum13["delRange3159Perc"] = round((delCatNum13["delRange3159"] / delCatNum13["fltTotal"]) * 100, 2)
delCatNum13["delRange0100Perc"] = round((delCatNum13["delRange0100"] / delCatNum13["fltTotal"]) * 100, 2)
delCatNum13["delRange0200Perc"] = round((delCatNum13["delRange0200"] / delCatNum13["fltTotal"]) * 100, 2)
delCatNum13["delRange0400Perc"] = round((delCatNum13["delRange0400"] / delCatNum13["fltTotal"]) * 100, 2)
delCatNum13["otp"] = round(100 - (delCatNum13["delRange1630Perc"] + delCatNum13["delRange3159Perc"] + delCatNum13["delRange0100Perc"] + delCatNum13["delRange0200Perc"] + delCatNum13["delRange0400Perc"]), 2)

delCatNum15 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME","Main_Cat1","DlyCodeAsgn"]).agg(
    totalDelayAssigned = ("DlyCodeAsgn", "count"),
    totalMinDly1 = ("DLY1","sum"),
    totalMinDly2 = ("DLY2","sum"),
    totalMinDly3 = ("DLY3","sum"),
    totalMinDly4 = ("DLY4","sum")
).reset_index()

delCatNum15["totalDelayMinutePerDelayCode"] = delCatNum15["totalMinDly1"] + delCatNum15["totalMinDly2"] + delCatNum15["totalMinDly3"] + delCatNum15["totalMinDly4"]

monthlyMetrics = df2.groupby(["YEAR", "MONTH_NUMBER", "MONTH_NAME"]).agg(
    minuteDelayTotalPerMonth = ("DelTotDep", "sum"),
    totalFlightPerMonth = ("FVal", lambda x: (x == "val").sum()),
    delayFlightPerMonth = ("DelVal", lambda x: (x == "late").sum())
).reset_index()

delCatNum15 = delCatNum15.merge(monthlyMetrics, on=["YEAR","MONTH_NUMBER","MONTH_NAME"], how="left")

delCatNum15["delayCodePercentage"] = 100 * ((delCatNum15["totalDelayMinutePerDelayCode"] / delCatNum15["minuteDelayTotalPerMonth"]) * (delCatNum15["delayFlightPerMonth"]/delCatNum15["totalFlightPerMonth"]))
delCatNum15["delayCodePercentage"] = delCatNum15["delayCodePercentage"].round(2)

delCatNum16 = df2.groupby(["YEAR","MONTH_NUMBER","MONTH_NAME","ZONE"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    onTimeFlights = ("DelVal", lambda x: (x == "on_time").sum()),
    delayFlights = ("DelVal", lambda x: (x == "late").sum())
).reset_index()

delCatNum16["otpDepPerFlightZonePerMonth"] = 100 * (delCatNum16["onTimeFlights"] / delCatNum16["fltTotal"])
delCatNum16["otpDepPerFlightZonePerMonth"] = delCatNum16["otpDepPerFlightZonePerMonth"].round(2)

delCatNum17 = df2.groupby(["YEAR","ZONE"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    onTimeFlights = ("DelVal", lambda x: (x == "on_time").sum()),
    delayFlights = ("DelVal", lambda x: (x == "late").sum())
).reset_index()

delCatNum17["otpDepPerFlightZonePerMonth"] = 100 * (delCatNum17["onTimeFlights"] / delCatNum17["fltTotal"])
delCatNum17["otpDepPerFlightZonePerMonth"] = delCatNum17["otpDepPerFlightZonePerMonth"].round(2)

# Generating output file from aggregated table to CSV files
save_path = os.path.join(output_folder, "otp_per_date_output.csv")
otpPerDate.to_csv(save_path, sep=";", index=False)

save_path2 = os.path.join(output_folder, "delay_category_output.csv")
delCatNum.to_csv(save_path2, sep=";", index=False)

save_path3 = os.path.join(output_folder, "otp_per_month_output.csv")
otpPerMonth.to_csv(save_path3, sep=";", index=False)

save_path4 = os.path.join(output_folder, "delay_category_per_month_output.csv")
delCatNum2.to_csv(save_path4, sep=";", index=False)

save_path5 = os.path.join(output_folder, "otp_per_station_per_month.csv")
delCatNum3.to_csv(save_path5, sep=";", index=False)

save_path6 = os.path.join(output_folder, "otp_per_station_per_date.csv")
delCatNum4.to_csv(save_path6, sep=";", index=False)

save_path7 = os.path.join(output_folder, "otp_per_station_class_per_month.csv")
delCatNum5.to_csv(save_path7, sep=";", index=False)

save_path8 = os.path.join(output_folder, "otp_per_station_class_per_date.csv")
delCatNum6.to_csv(save_path8, sep=";", index=False)

save_path9 = os.path.join(output_folder, "dfs_details.csv")
df2.to_csv(save_path9, sep=";", index=False)

save_path10 = os.path.join(output_folder, "delay_per_cat_per_time.csv")
delCatNum9.to_csv(save_path10, sep=";", index=False)

save_path11 = os.path.join(output_folder, "otp_arr_per_date_output.csv")
otpArrPerDate.to_csv(save_path11, sep=";", index=False)

save_path12 = os.path.join(output_folder, "otp_arr_per_month_output.csv")
otpArrPerMonth.to_csv(save_path12, sep=";", index=False)

save_path13 = os.path.join(output_folder, "delay_category_arrival_output.csv")
delCatNum10.to_csv(save_path13, sep=";", index=False)

save_path14 = os.path.join(output_folder, "delay_category_arrival_per_month_output.csv")
delCatNum11.to_csv(save_path14, sep=";", index=False)

save_path15 = os.path.join(output_folder, "otp_arr_per_station_per_month.csv")
delCatNum12.to_csv(save_path15, sep=";", index=False)

save_path16 = os.path.join(output_folder, "otp_arr_per_station_per_date.csv")
delCatNum13.to_csv(save_path16, sep=";", index=False)

save_path17 = os.path.join(output_folder, "delay_category_per_year_output.csv")
delCatNum14.to_csv(save_path17, sep=";", index=False)

save_path18 = os.path.join(output_folder, "assigned_delay_code_per_month.csv")
delCatNum15.to_csv(save_path18, sep=";", index=False)

save_path19 = os.path.join(output_folder, "otpPerFlightZoneMonthly.csv")
delCatNum16.to_csv(save_path19, sep=";", index=False)

save_path20 = os.path.join(output_folder, "otpPerFlightZoneYearly.csv")
delCatNum17.to_csv(save_path20, sep=";", index=False)