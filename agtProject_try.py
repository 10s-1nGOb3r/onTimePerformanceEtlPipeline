import pandas as pd
import numpy as np
import os

# Setting up the file path to be export later
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "input_try", "pyActGt_try.csv")
file_path2 = os.path.join(script_dir, "input_try", "station_db.csv")
save_at = os.path.join(script_dir, "output", "sgtDetails.csv")
save_at2 = os.path.join(script_dir, "output", "agtDetails.csv")
save_at3 = os.path.join(script_dir, "output", "sgtAgtDetails.csv")
save_at4 = os.path.join(script_dir, "output", "agtPerDate.csv")
save_at5 = os.path.join(script_dir, "output", "agtPerStationPerDate.csv")
save_at6 = os.path.join(script_dir, "output", "agtPerMonth.csv")
save_at7 = os.path.join(script_dir, "output", "agtPerStationPerMonth.csv")
save_at8 = os.path.join(script_dir, "output", "agtPerClassPerMonth.csv")
save_at9 = os.path.join(script_dir, "output", "agtPerClassPerDate.csv")

# Scanning files
df = pd.read_csv(file_path,sep=";")

# Start with data cleansing and data formatting
df["DATE"] = pd.to_datetime(df["DATE"], format="%d/%m/%Y", errors="coerce")
df["MONTH_NUMBER"] = df["DATE"].dt.month
df["MONTH_NAME"] = df["DATE"].dt.month_name()
df["YEAR"] = df["DATE"].dt.year
df["DEP"] = df["DEP"].astype("string")
df["ActBlockOff"] = pd.to_datetime(df["ActBlockOff"], format="%d/%m/%Y", errors="coerce")
df["ActBlockOn"] = pd.to_datetime(df["ActBlockOn"], format="%d/%m/%Y", errors="coerce")
df["StdBOffTime"] = pd.to_datetime(df["DATE"].dt.strftime('%Y-%m-%d') + ' ' + df["STD"])
df["StdBOnTime"] = pd.to_datetime(df["DATE"].dt.strftime('%Y-%m-%d') + ' ' + df["STA"])
df["AtdBOffTime"] = pd.to_datetime(df["ActBlockOff"].dt.strftime('%Y-%m-%d') + ' ' + df["ATD"])
df["AtaBOnTime"] = pd.to_datetime(df["ActBlockOn"].dt.strftime('%Y-%m-%d') + ' ' + df["ATA"])
df["ST"] = df["ST"].fillna("0")
df["ST"] = df["ST"].astype("string")
df["EarlyLandVal"] = np.where(df["StdBOnTime"] > df["AtaBOnTime"], "early",  "0")
df["EarlyLandVal"] = df["EarlyLandVal"].astype("string")

# Validating for counted flight and delayed flight logic
FValCond = ((df["TYPE"] == "J") | (df["TYPE"] == "G")) & (df["ST"] == "0")
df["FVal"] = np.where(FValCond, "val", "not_count")

# Sorting table for Scheduled Ground Time calculation
df = df.sort_values(by=["REG", "StdBOffTime"], ascending=[True, True])

# Defining Aircraft Rotation Part for Scheduled Ground Time Calculation Table
df["RotPart"] = np.where((df["DATE"].shift(1) != df["DATE"]) & (df["DATE"].shift(-1) == df["DATE"]), "head",
                        np.where((df["DATE"].shift(1) == df["DATE"]) & (df["DATE"].shift(-1) == df["DATE"]), "body",
                        np.where((df["DATE"].shift(1) == df["DATE"]) & (df["DATE"].shift(-1) != df["DATE"]), "tail", 
                        np.where((df["DATE"].shift(1) != df["DATE"]) & (df["DATE"].shift(-1) != df["DATE"]), "head&tail", "0")))) 

df["RotPart"] = df["RotPart"].astype("string")

# Defining the logic to calculate Scheduled Ground Time
df["SchedGT"] = np.where((df["RotPart"] == "head"), 0,
                         np.where((df["RotPart"] == "body") & (df["EarlyLandVal"].shift(1) == "0"), df["StdBOffTime"] - df["StdBOnTime"].shift(1), 
                         np.where((df["RotPart"] == "body") & (df["EarlyLandVal"].shift(1) == "early"), df["StdBOffTime"] - df["AtaBOnTime"].shift(1), 
                         np.where((df["RotPart"] == "tail") & (df["EarlyLandVal"].shift(1) == "0"), df["StdBOffTime"] - df["StdBOnTime"].shift(1),
                         np.where((df["RotPart"] == "tail") & (df["EarlyLandVal"].shift(1) == "early"), df["StdBOffTime"] - df["AtaBOnTime"].shift(1),
                         np.where(df["RotPart"] == "head&tail", 0,0))))))

# Defining the primary key to merge Scheduled Ground Time table and Actual Ground Time table
df["DATE2"] = df["DATE"].astype("string")
df["keyActGT"] = df["DATE2"] + "." + df["FLT"] + "." + df["DEP"] + "." + df["ARR"]
df["keyActGT"] = df["keyActGT"].astype("string")

# Reading the file for Actual Ground Time Table
file_path = os.path.join(script_dir, "input_try", "pyActGt_try.csv")

df2 = pd.read_csv(file_path,sep=";")

# Data cleansing and data formatting
df2["DATE"] = pd.to_datetime(df2["DATE"], format="%d/%m/%Y", errors="coerce")
df2["ActBlockOff"] = pd.to_datetime(df2["ActBlockOff"], format="%d/%m/%Y", errors="coerce")
df2["ActBlockOn"] = pd.to_datetime(df2["ActBlockOn"], format="%d/%m/%Y", errors="coerce")
df2["StdBOffTime"] = pd.to_datetime(df2["DATE"].dt.strftime('%Y-%m-%d') + ' ' + df2["STD"])
df2["StdBOnTime"] = pd.to_datetime(df2["DATE"].dt.strftime('%Y-%m-%d') + ' ' + df2["STA"])
df2["AtdBOffTime"] = pd.to_datetime(df2["ActBlockOff"].dt.strftime('%Y-%m-%d') + ' ' + df2["ATD"])
df2["AtaBOnTime"] = pd.to_datetime(df2["ActBlockOn"].dt.strftime('%Y-%m-%d') + ' ' + df2["ATA"])
df2["ST"] = df2["ST"].fillna("0")
df2["ST"] = df2["ST"].astype("string")
df2["EarlyLandVal"] = np.where(df2["StdBOnTime"] > df2["AtaBOnTime"], "early",  "0")
df2["EarlyLandVal"] = df2["EarlyLandVal"].astype("string")

# Sorting table for Actual Ground Time Calculation
df2 = df2.sort_values(by=["REG", "AtdBOffTime"], ascending=[True, True])

# Defining Aircraft Rotation Part for Actual Ground Time Calculation Table
df2["RotPart"] = np.where((df2["DATE"].shift(1) != df2["DATE"]) & (df2["DATE"].shift(-1) == df2["DATE"]), "head",
                        np.where((df2["DATE"].shift(1) == df2["DATE"]) & (df2["DATE"].shift(-1) == df2["DATE"]), "body",
                        np.where((df2["DATE"].shift(1) == df2["DATE"]) & (df2["DATE"].shift(-1) != df2["DATE"]), "tail", 
                        np.where((df2["DATE"].shift(1) != df2["DATE"]) & (df2["DATE"].shift(-1) != df2["DATE"]), "head&tail", "0")))) 

df2["RotPart"] = df2["RotPart"].astype("string")

# Defining the logic to calculate Actual Ground Time
df2["ActualGT"] = np.where((df2["RotPart"] == "head"), df2["AtdBOffTime"] - df2["StdBOffTime"],
                         np.where((df2["RotPart"] == "head&tail"), df2["AtdBOffTime"] - df2["StdBOffTime"],
                         np.where((df2["RotPart"] == "body") & (df2["EarlyLandVal"].shift(1) == "0"), df2["AtdBOffTime"] - df2["AtaBOnTime"].shift(1), 
                         np.where((df2["RotPart"] == "body") & (df2["EarlyLandVal"].shift(1) == "early"), df2["AtdBOffTime"] - df2["AtaBOnTime"].shift(1), 
                         np.where((df2["RotPart"] == "tail") & (df2["EarlyLandVal"].shift(1) == "0"), df2["AtdBOffTime"] - df2["AtaBOnTime"].shift(1),
                         np.where((df2["RotPart"] == "tail") & (df2["EarlyLandVal"].shift(1) == "early"), df2["AtdBOffTime"] - df2["AtaBOnTime"].shift(1),0))))))

# Defining the primary key to be merged with Scheduled Ground Time table
df2["DATE2"] = df2["DATE"].astype("string")
df2["keyActGT"] = df2["DATE2"] + "." + df2["FLT"] + "." + df2["DEP"] + "." + df2["ARR"]
df2["keyActGT"] = df2["keyActGT"].astype("string")

# Merge the two tables : Scheduled Ground Time Table & Actual Ground Time Table
df2_clean = df2.drop_duplicates(subset=["keyActGT"])
df_final = pd.merge(df, df2_clean[["keyActGT", "ActualGT"]], on="keyActGT", how="left")

# Define the logic by comparing two fields : SchedGT & ActualGT
df_final["AGT"] = np.where((df_final["SchedGT"] < df_final["ActualGT"]) & (df_final["FVal"] == "val"), "> SGT",
                        np.where((df_final["SchedGT"] == df_final["ActualGT"]) & (df_final["FVal"] == "val"), "E SGT",
                        np.where((df_final["SchedGT"] > df_final["ActualGT"])  & (df_final["FVal"] == "val"), "< SGT", "0")))

df_final["AGT"] = df_final["AGT"].astype("string")

# Merge the ground table with station table
station_db = pd.read_csv(file_path2,sep=";")
station_db["STATION"] = station_db["STATION"].astype("string")

df_final = pd.merge(df_final, station_db[["STATION", "TOWN", "CLASS"]], left_on="DEP",right_on="STATION",how="left")

df_final["AIRPORT_TOWN"] = df_final["DEP"] + " - " + df_final["TOWN"]

# Aggregate the table based on the requirements
groundTimePerDate = df_final.groupby(["DATE"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    lessAGT = ("AGT", lambda x: (x == "< SGT").sum()),
    equalAGT = ("AGT", lambda x: (x == "E SGT").sum()),
    moreAGT = ("AGT", lambda x: (x == "> SGT").sum())
).reset_index()

groundTimePerDate["lessAGTPerc"] = round((groundTimePerDate["lessAGT"] / groundTimePerDate["fltTotal"]) * 100, 2)
groundTimePerDate["equalAGTPerc"] = round((groundTimePerDate["equalAGT"] / groundTimePerDate["fltTotal"]) * 100, 2)
groundTimePerDate["moreAGTPerc"] = round((groundTimePerDate["moreAGT"] / groundTimePerDate["fltTotal"]) * 100, 2)

groundTimePerMonth = df_final.groupby(["YEAR", "MONTH_NUMBER", "MONTH_NAME"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    lessAGT = ("AGT", lambda x: (x == "< SGT").sum()),
    equalAGT = ("AGT", lambda x: (x == "E SGT").sum()),
    moreAGT = ("AGT", lambda x: (x == "> SGT").sum())
).reset_index()

groundTimePerMonth["lessAGTPerc"] = round((groundTimePerMonth["lessAGT"] / groundTimePerMonth["fltTotal"]) * 100, 2)
groundTimePerMonth["equalAGTPerc"] = round((groundTimePerMonth["equalAGT"] / groundTimePerMonth["fltTotal"]) * 100, 2)
groundTimePerMonth["moreAGTPerc"] = round((groundTimePerMonth["moreAGT"] / groundTimePerMonth["fltTotal"]) * 100, 2)

groundTimePerStationPerMonth = df_final.groupby(["YEAR", "MONTH_NUMBER", "MONTH_NAME", "CLASS", "AIRPORT_TOWN"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    lessAGT = ("AGT", lambda x: (x == "< SGT").sum()),
    equalAGT = ("AGT", lambda x: (x == "E SGT").sum()),
    moreAGT = ("AGT", lambda x: (x == "> SGT").sum())
).reset_index()

groundTimePerStationPerMonth["lessAGTPerc"] = round((groundTimePerStationPerMonth["lessAGT"] / groundTimePerStationPerMonth["fltTotal"]) * 100, 2)
groundTimePerStationPerMonth["equalAGTPerc"] = round((groundTimePerStationPerMonth["equalAGT"] / groundTimePerStationPerMonth["fltTotal"]) * 100, 2)
groundTimePerStationPerMonth["moreAGTPerc"] = round((groundTimePerStationPerMonth["moreAGT"] / groundTimePerStationPerMonth["fltTotal"]) * 100, 2)

groundTimePerStationPerDate = df_final.groupby(["DATE", "CLASS", "AIRPORT_TOWN"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    lessAGT = ("AGT", lambda x: (x == "< SGT").sum()),
    equalAGT = ("AGT", lambda x: (x == "E SGT").sum()),
    moreAGT = ("AGT", lambda x: (x == "> SGT").sum())
).reset_index()

groundTimePerStationPerDate["lessAGTPerc"] = round((groundTimePerStationPerDate["lessAGT"] / groundTimePerStationPerDate["fltTotal"]) * 100, 2)
groundTimePerStationPerDate["equalAGTPerc"] = round((groundTimePerStationPerDate["equalAGT"] / groundTimePerStationPerDate["fltTotal"]) * 100, 2)
groundTimePerStationPerDate["moreAGTPerc"] = round((groundTimePerStationPerDate["moreAGT"] / groundTimePerStationPerDate["fltTotal"]) * 100, 2)

groundTimePerClassPerMonth = df_final.groupby(["YEAR", "MONTH_NUMBER", "MONTH_NAME", "CLASS"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    lessAGT = ("AGT", lambda x: (x == "< SGT").sum()),
    equalAGT = ("AGT", lambda x: (x == "E SGT").sum()),
    moreAGT = ("AGT", lambda x: (x == "> SGT").sum())
).reset_index()

groundTimePerClassPerMonth["lessAGTPerc"] = round((groundTimePerClassPerMonth["lessAGT"] / groundTimePerClassPerMonth["fltTotal"]) * 100, 2)
groundTimePerClassPerMonth["equalAGTPerc"] = round((groundTimePerClassPerMonth["equalAGT"] / groundTimePerClassPerMonth["fltTotal"]) * 100, 2)
groundTimePerClassPerMonth["moreAGTPerc"] = round((groundTimePerClassPerMonth["moreAGT"] / groundTimePerClassPerMonth["fltTotal"]) * 100, 2)

groundTimePerClassPerDate = df_final.groupby(["DATE", "CLASS"]).agg(
    fltTotal = ("FVal", lambda x: (x == "val").sum()),
    lessAGT = ("AGT", lambda x: (x == "< SGT").sum()),
    equalAGT = ("AGT", lambda x: (x == "E SGT").sum()),
    moreAGT = ("AGT", lambda x: (x == "> SGT").sum())
).reset_index()

groundTimePerClassPerDate["lessAGTPerc"] = round((groundTimePerClassPerDate["lessAGT"] / groundTimePerClassPerDate["fltTotal"]) * 100, 2)
groundTimePerClassPerDate["equalAGTPerc"] = round((groundTimePerClassPerDate["equalAGT"] / groundTimePerClassPerDate["fltTotal"]) * 100, 2)
groundTimePerClassPerDate["moreAGTPerc"] = round((groundTimePerClassPerDate["moreAGT"] / groundTimePerClassPerDate["fltTotal"]) * 100, 2)

# Exporting files into CSV format

df.to_csv(save_at, sep=";", index=False)
df2.to_csv(save_at2, sep=";", index=False)
df_final.to_csv(save_at3, sep=";", index=False)
groundTimePerDate.to_csv(save_at4, sep=";", index=False)
groundTimePerStationPerDate.to_csv(save_at5, sep=";", index=False)
groundTimePerMonth.to_csv(save_at6, sep=";", index=False)
groundTimePerStationPerMonth.to_csv(save_at7, sep=";", index=False)
groundTimePerClassPerMonth.to_csv(save_at8, sep=";", index=False)
groundTimePerClassPerDate.to_csv(save_at9, sep=";", index=False)