# %%
import pandas as pd
from glob import glob
import os
import numpy as np
from datetime import datetime
import re

# %%
folder_path = os.path.join("..", "data", "childcare centers", "20*")
folders = glob(folder_path)
files = [
    glob(os.path.join(folder + '/*')) for folder in folders
]
files = [item for sublist in files for item in (sublist if isinstance(sublist, list) else [sublist])]
# %%
def month_name_to_iso(datestring: str) -> str:
  # Convert date string to datetime object
  date_obj = datetime.strptime(datestring, '%B %Y')
  # Convert datetime object to string in desired format
  return datetime.strftime(date_obj, '%m-%Y')

def age_string_to_year_fraction(age_string: str) -> float:
  # convert N Year(s), I Month(s), J Week(S) to N + I/12 + J/52
  pattern = r"(\d+) Year\(s\), (\d+) Month\(s\), (\d+) Week\(s\)"
  match = re.match(pattern, age_string)

  if match:
      year = int(match.group(1))
      month = int(match.group(2))
      week = int(match.group(3))
      return year + month/12 + week/52
# %%
def extract_data(file: str) -> pd.DataFrame:
  # Read Excel file
  excel_file = pd.ExcelFile(file)
  # Get sheet names
  sheet_names = excel_file.sheet_names
  # Check if there are multiple sheets
  if len(sheet_names) > 1:
    #  read each sheet
    # find sheet name that contains 'data'
    for sheet_name in sheet_names:
      sheet_lower = sheet_name.lower()  
      if 'directory' in sheet_lower or 'raw' in sheet_lower or 'state' in sheet_lower or 'wisconsin' in sheet_lower:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    if 'df' not in locals():
      print("Failed to find sheet with 'directory' or 'raw' or 'state' in name in: ", file)
      return None
  else:
      df = pd.read_excel(file)

  if "Facility Name" in df.columns:
    return df
  else: 
    column_row_index = None
    index = 0
    while column_row_index == None and index < len(df):
      values = df.iloc[index].values
      if "Facility Name" in values:
        column_row_index = index
        # set columns
        df.columns = df.iloc[column_row_index]
        # slice df to get columns
        df = df.iloc[column_row_index+1:]
      index += 1

  columns = df.columns
  # if any column np.isnan
  for column in columns:
    if type(column) != str and np.isnan(column):
      df = df.drop(columns=column)
    
  # assign month
  # eg. convert April 2022 to 04-2022
  try:
    datestring = month_name_to_iso(file.split("_")[-1].split(".")[0].split(" - ")[0].strip())
    df['Date'] = datestring
  except: 
    print("Failed to parse date in: ", file)
    return None

  # convert min and max age to year fraction
  df['Min Age'] = df['From Age'].apply(age_string_to_year_fraction)
  df['Max Age'] = df['To Age'].apply(age_string_to_year_fraction)

  return df
# %%
dfs = []
for file in files:
  df = extract_data(file)
  if df is not None:
    dfs.append(df)


# %%
combined = pd.concat(dfs)

# %%
deduped = combined.drop_duplicates(['Line Address 1', 'Line Address 2', 'City', 'Zip Code'], keep="first")
columns = [
  'Line Address 1', 'Line Address 2', 'City', 'Zip Code'
]
deduped['ADDRESS'] = deduped['Line Address 1'] + " " + deduped['Line Address 2']
deduped = deduped[['ADDRESS', 'City', 'Zip Code']]
deduped = deduped.reset_index()
deduped = deduped.rename(columns={
  'City': 'CITY',
  'Zip Code': 'ZIP',
  'index': 'ID'
})
# %%
deduped.to_csv("../data/to_geocode.csv", index=False)
# %%
