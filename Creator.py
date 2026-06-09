import glob
import os
from datetime import datetime, timedelta
import pandas as pd
import geopandas as gpd

# ------------------------
input_folder = "logs"
output_file = "positions.gpkg"
layer_name = "PlayerPositions"
y_Offset = 11195 # change this to the zomboid choordinate where you flip the y axis. The Zomboid Y equal to this is 0

world_epoch = pd.Timestamp(datetime(2020, 1, 1, 0, 0, 0))

excluded_users_Username = {"Player1", "TestUser", "BotAccount", "WandaJustice"} # Include usernames for which data should be deleted

# Read files into series
all_files = glob.glob(os.path.join(input_folder, "*.txt"))
lines = []
for f in all_files:
    with open(f, encoding="utf-8") as infile:
        lines.extend(infile.readlines())

lines = pd.Series(lines).str.strip()

# ---------------------------
pattern = r"\[(.*?)\]\s+([^,]+),([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)"
df = lines.str.extract(pattern)
df.columns = ["LogTime", "Username", "WorldHours", "dwell_heatmap",
              "dwell_movement", "movement", "speed", "visible_zombies", "X", "Y"]
print("Working...")

# remove excluded users 
df = df[~df["Username"].isin(excluded_users_Username)]

numeric_cols = ["WorldHours", "dwell_heatmap", "dwell_movement", "movement", "speed", "visible_zombies", "X", "Y"]
df[numeric_cols] = df[numeric_cols].astype(float)


# Do y offset and time conversion
df["Y"] = y_Offset - df["Y"]
df["LogTime"] = pd.to_datetime(df["LogTime"], format="%d-%m-%y %H:%M:%S.%f", errors="raise")
df["WorldTime"] = world_epoch + pd.to_timedelta(df["WorldHours"], unit="h")

print("Working...")

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["X"], df["Y"]), crs=None)

print("Working...")

# SAve to GeoPackage

gdf.to_file(output_file, layer=layer_name, driver="GPKG")
print("Done! GeoPackage saved")