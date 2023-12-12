import os
os.environ['USE_PYGEOS'] = '0'
import pandas as pd
import geopandas as gpd
from glob import glob
import numpy as np
from datetime import datetime
import re
from typing import List


class ChildcareDataParser:
  dfs: List[pd.DataFrame] = []
  combined: pd.DataFrame
  # geo
  geocoded: gpd.GeoDataFrame
  assembly: gpd.GeoDataFrame
  senate_districts: gpd.GeoDataFrame
  congressional_districts: gpd.GeoDataFrame
  tracts: gpd.GeoDataFrame
  counties: gpd.GeoDataFrame
  # util
  data_dir: str

  def __init__(self, files: List[str], data_dir:str):
    self.data_dir = data_dir
    for file in files:
      df = self.extract_data(file)
      if df is not None:
        self.dfs.append(df)

  def extract_data(self, file: str) -> pd.DataFrame:
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
      datestring = self.month_name_to_iso(file.split("_")[-1].split(".")[0].split(" - ")[0].strip())
      df['Date'] = datestring
    except: 
      print("Failed to parse date in: ", file)
      return None

    # convert min and max age to year fraction
    df['Min Age'] = df['From Age'].apply(self.age_string_to_year_fraction)
    df['Max Age'] = df['To Age'].apply(self.age_string_to_year_fraction)

    return df
  
  def month_name_to_iso(self, datestring: str) -> str:
    # Convert date string to datetime object
    date_obj = datetime.strptime(datestring, '%B %Y')
    # Convert datetime object to string in desired format
    return datetime.strftime(date_obj, '%m-%Y')

  def age_string_to_year_fraction(self, age_string: str) -> float:
    # convert N Year(s), I Month(s), J Week(S) to N + I/12 + J/52
    pattern = r"(\d+) Year\(s\), (\d+) Month\(s\), (\d+) Week\(s\)"
    match = re.match(pattern, age_string)

    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        week = int(match.group(3))
        return year + month/12 + week/52
  
  def clean_gdf_join(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if "index_right" in gdf.columns:
      gdf = gdf.drop(columns=["index_right"])
    if "index_left" in gdf.columns:
      gdf = gdf.drop(columns=["index_left"])
    return gdf
  
  def merge_data(self):
    self.combined = pd.concat(self.dfs)
    self.combined['Address'] = self.combined['Line Address 1'] + " " + self.combined['Line Address 2'] 
    
  def load_geo(self):
    # geocoded providers
    deduped = self.combined.drop_duplicates(['Line Address 1', 'Line Address 2', 'City', 'Zip Code'], keep="first")
    provider_ids = deduped['Provider Number'].values
    location_ids = deduped['Location Number'].values
    
    self.geocoded = pd.read_csv(os.path.join(self.data_dir, "geocoded.csv"))
    self.geocoded['Provider Number'] = provider_ids
    self.geocoded['Location Number'] = location_ids
    self.geocoded = gpd.GeoDataFrame(
        self.geocoded, geometry=gpd.points_from_xy(self.geocoded.Longitude, self.geocoded.Latitude))
    self.geocoded = self.geocoded.set_crs("EPSG:4326")
    
    self.assembly = gpd.read_file(os.path.join(self.data_dir, 'geo', 'WI_Assembly_Districts_2022','WI_Assembly_Districts_2022.shp'))
    self.senate_districts = gpd.read_file(os.path.join(self.data_dir, 'geo', 'Wisconsin_Senate_Districts_(2022)','Wisconsin_Senate_Districts_(2022).shp'))
    self.congressional_districts = gpd.read_file(os.path.join(self.data_dir, 'geo', 'WI_Congressional_Districts_2002','WI_Congressional_Districts_2002.shp'))
    self.tracts = gpd.read_file(os.path.join(self.data_dir, 'geo', 'tracts_2021.parquet'))
    self.counties = gpd.read_file(os.path.join(self.data_dir, 'geo', 'counties_2019.parquet'))
    self.counties = self.counties[self.counties['STATEFP'] == '55']
    self.counties = self.counties.to_crs("EPSG:4326")
    self.assembly = self.assembly.to_crs("EPSG:4326")
    self.senate_districts = self.senate_districts.to_crs("EPSG:4326")
    self.congressional_districts = self.congressional_districts.to_crs("EPSG:4326")
    self.tracts = self.tracts.to_crs("EPSG:4326")

  def sjoin_providers(self):
    sjoin_assembly = self.assembly[['ASM2021', 'SEN2021', 'geometry']]
    sjoin_county = self.counties[['NAMELSAD', 'geometry']]
    sjoin_senate = self.senate_districts[['SEN2021', 'SEN_NUM', 'geometry']]
    sjoin_senate = sjoin_senate.rename(columns={
      'SEN2021': 'SENATE_DISTRICT2021',
      'SEN_NUM': 'SENATE_DISTRICT'
    })
    sjoin_congressional = self.congressional_districts[['DISTRICT', 'geometry']]
    sjoin_congressional = sjoin_congressional.rename(columns={
      'DISTRICT': 'CONGRESSIONAL_DISTRICT'
    })
    sjoin_tracts = self.tracts[['GEOID', 'geometry']]

    for df in [sjoin_assembly, sjoin_county, sjoin_senate, sjoin_congressional, sjoin_tracts]:
      self.geocoded = gpd.sjoin(self.geocoded, df, how="left", op="within")
      self.geocoded = self.clean_gdf_join(self.geocoded)
    self.geocoded = self.geocoded.drop_duplicates(['ADDRESS',"Provider Number"])
    for col in ['Provider Number', 'Location Number']:
      self.geocoded[col] = self.geocoded[col].astype(str)
      
  def clean_combined(self):
    for col in ['Provider Number', 'Location Number', 'Facility Number']:
      self.combined[col] = self.combined[col].astype(str)

    self.combined['Date'] = self.combined['Date'].str.split('-').str[1] + "-" + self.combined['Date'].str.split('-').str[0]

  def output_data(self):
    # today's date iso MM-YYYY
    today = datetime.today().strftime('%m-%Y')
    self.combined.to_parquet(os.path.join(self.data_dir, 'output', f"combined_LCC_CCC_Registtry_{today}.parquet"), index=False)
    self.geocoded.to_parquet(os.path.join(self.data_dir, 'output', f"geocoded_providers_{today}.parquet"), index=False)
    self.combined.to_csv(os.path.join(self.data_dir, 'output', f"combined_LCC_CCC_Registtry_{today}.csv"), index=False)
    self.geocoded.to_csv(os.path.join(self.data_dir, 'output', f"geocoded_providers_{today}.csv"), index=False)

  def output_geo(self):
    self.assembly.to_parquet(os.path.join(self.data_dir, 'output', "assembly.parquet"))
    self.senate_districts.to_parquet(os.path.join(self.data_dir, 'output', "senate_districts.parquet"))
    self.congressional_districts.to_parquet(os.path.join(self.data_dir, 'output', "congressional_districts.parquet"))
    self.tracts.to_parquet(os.path.join(self.data_dir, 'output', "tracts.parquet"))
    self.counties.to_parquet(os.path.join(self.data_dir, 'output', "counties.parquet"))

def main():
  data_dir = os.path.join(os.getcwd(), "data")

  folder_path = os.path.join(data_dir, "childcare centers", "20*")
  folders = glob(folder_path)
  files = [
      glob(os.path.join(folder + '/*')) for folder in folders
  ]
  files = [item for sublist in files for item in (sublist if isinstance(sublist, list) else [sublist])]

  data_parser = ChildcareDataParser(files, data_dir)
  data_parser.merge_data()
  data_parser.load_geo()
  data_parser.sjoin_providers()
  data_parser.clean_combined()
  data_parser.output_data()

if __name__ == "__main__":
    main()