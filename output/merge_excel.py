import pandas as pd
import glob
import os

# Set the directory where the Excel files are located
directory = "D:/Генетичні алгоритми/EA-Lab/out/tables"

# Get a list of all Excel files in the directory
excel_files = glob.glob(os.path.join(directory, '*.xlsx'))

excel_files = sorted(excel_files)

# Create an empty list to store the data frames
dfs = []

# Loop through each Excel file and read it into a data frame
for file in excel_files:
    df = pd.read_excel(file)
    dfs.append(df)

# Concatenate the data frames vertically
merged_df = pd.concat(dfs, ignore_index=True)

# Write the merged data frame to a new Excel file
merged_df.to_excel('aggregated.xlsx', index=False)