import os
os.environ['USE_PYGEOS'] = '0'
import pandas as pd

cols_to_keep = {
  'FIPS':'FIPS',
  'Civilian Population in Labor Force 16 Years and Over:':'Pop 16+',
  'Civilian Population in Labor Force 16 Years and Over: Employed':'Pop 16+ Employed',
  'Civilian Population in Labor Force 16 Years and Over: Unemployed':'Pop 16+ Unemployed',
  'Population 25 Years and Over:':'Pop 25+',
  'Population 25 Years and Over: Less than High School':'Pop 25+ Less than High School',
  'Population 25 Years and Over: High School Graduate or More (Includes Equivalency)':'Pop 25+ High School Graduate or More (Includes Equivalency)',
  'Population 25 Years and Over: Some College or More':'Pop 25+ Some College or More',
  "Population 25 Years and Over: Bachelor's Degree or More":"Population 25 Years and Over: Bachelor's Degree or More",
  "Population 25 Years and Over: Master's Degree or More":"Population 25 Years and Over: Master's Degree or More",
  'Population 25 Years and Over: Professional School Degree or More':'Pop 25+ Professional School Degree or More',
  'Population 25 Years and Over: Doctorate Degree':'Pop 25+ Doctorate Degree',
  'Median Household Income (In 2021 Inflation Adjusted Dollars)':'Median Household Income (In 2021 Inflation Adjusted Dollars)',
  'Total Population':'Total Population',
  'Total Population: Not Hispanic or Latino':'Pop NH',
  'Total Population: Not Hispanic or Latino: White Alone':'Pop NH: White Alone',
  'Total Population: Not Hispanic or Latino: Black or African American Alone':'Pop NH: Black or African American Alone',
  'Total Population: Not Hispanic or Latino: American Indian and Alaska Native Alone':'Pop NH: American Indian and Alaska Native Alone',
  'Total Population: Not Hispanic or Latino: Asian Alone':'Pop NH: Asian Alone',
  'Total Population: Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone':'Pop NH: Native Hawaiian and Other Pacific Islander Alone',
  'Total Population: Not Hispanic or Latino: Some Other Race Alone':'Pop NH: Some Other Race Alone',
  'Total Population: Not Hispanic or Latino: Two or More Races':'Pop NH: Two or More Races',
  'Total Population: Hispanic or Latino':'Total Population: Hispanic or Latino',
  'Total':'Total',
  'Total: Under 6 Years':'Pop Under 6',
  'Total: Under 6 Years: Living With Two Parents':'Pop Under 6 Living With Two Parents',
  'Total: Under 6 Years: Living With Two Parents: Both Parents In Labor Force':'Pop Under 6 Living With Two Parents: Both Parents In Labor Force',
  'Total: Under 6 Years: Living With Two Parents: Father Only In Labor Force':'Pop Under 6 Living With Two Parents: Father Only In Labor Force',
  'Total: Under 6 Years: Living With Two Parents: Mother Only In Labor Force':'Pop Under 6 Living With Two Parents: Mother Only In Labor Force',
  'Total: Under 6 Years: Living With Two Parents: Neither Parent In Labor Force':'Pop Under 6 Living With Two Parents: Neither Parent In Labor Force',
  'Total:  Living With One Parent':'Total: Living With One Parent',
  'Total:  Living With One Parent: Living With Father':'Total: Living With One Parent: Living With Father',
  'Total:  Living With One Parent: Living With Father: In Labor Force':'Total: Living With One Parent: Living With Father: In Labor Force',
  'Total:  Living With One Parent: Living With Father: Not In Labor Force':'Total: Living With One Parent: Living With Father: Not In Labor Force',
  'Total:   Living With Mother':'Total: Living With Mother',
  'Total:   Living With Mother: In Labor Force':'Total: Living With Mother: In Labor Force',
  'Total:   Living With Mother: Not In Labor Force':'Total: Living With Mother: Not In Labor Force',
  'Total: 6 To 17 Years':'Total: 6 To 17 Years',
  'Total: 6 To 17 Years: Living With Two Parents':'Total: 6 To 17 Years: Living With Two Parents',
  'Total: 6 To 17 Years: Living With Two Parents: Both Parents In Labor Force':'Total: 6 To 17 Years: Living With Two Parents: Both Parents In Labor Force',
  'Total: 6 To 17 Years: Living With Two Parents: Father Only In Labor Force':'Total: 6 To 17 Years: Living With Two Parents: Father Only In Labor Force',
  'Total: 6 To 17 Years: Living With Two Parents: Mother Only In Labor Force':'Total: 6 To 17 Years: Living With Two Parents: Mother Only In Labor Force',
  'Total: 6 To 17 Years: Living With Two Parents: Neither Parent In Labor Force':'Total: 6 To 17 Years: Living With Two Parents: Neither Parent In Labor Force',
  'Total:  Living With One Parent.1':'Total: Living With One Parent.1',
  'Total:  Living With One Parent: Living With Father.1':'Total: Living With One Parent: Living With Father.1',
  'Total:  Living With One Parent: Living With Father: In Labor Force.1':'Total: Living With One Parent: Living With Father: In Labor Force.1',
  'Total:  Living With One Parent: Living With Father: Not In Labor Force.1':'Total: Living With One Parent: Living With Father: Not In Labor Force.1',
  'Total:   Living With Mother.1':'Total: Living With Mother.1',
  'Total:   Living With Mother: In Labor Force.1':'Total: Living With Mother: In Labor Force.1',
  'Total:   Living With Mother: Not In Labor Force.1':'Total: Living With Mother: Not In Labor Force.1',
}


def handle_community_vars(data_dir: str):
  countyData = pd.read_csv(os.path.join(data_dir, 'community vars', 'wi-county.csv')).iloc[1:]
  assemblyDistrictData = pd.read_csv(os.path.join(data_dir, 'community vars', 'wi-assembly-districts.csv')).iloc[1:]
  senateDistricstData = pd.read_csv(os.path.join(data_dir, 'community vars', 'wi-senate-districts.csv')).iloc[1:]
  congressionalDistrictsData = pd.read_csv(os.path.join(data_dir, 'community vars', 'wi-congressional-districts.csv')).iloc[1:]
  tractsData = pd.read_csv(os.path.join(data_dir, 'community vars', 'wi-tracts.csv')).iloc[1:]
  zipData = pd.read_csv(os.path.join(data_dir, 'community vars', 'wi-zip.csv')).iloc[1:]
  zipData['FIPS'] = zipData['Qualifying Name'].str.split(' ').str[1]

  # keep only cols in cols_to_keep
  countyData = countyData[cols_to_keep.keys()]
  assemblyDistrictData = assemblyDistrictData[cols_to_keep.keys()]
  senateDistricstData = senateDistricstData[cols_to_keep.keys()]
  congressionalDistrictsData = congressionalDistrictsData[cols_to_keep.keys()]
  tractsData = tractsData[cols_to_keep.keys()]
  zipData = zipData[cols_to_keep.keys()]

  # rename
  countyData = countyData.rename(columns=cols_to_keep)
  assemblyDistrictData = assemblyDistrictData.rename(columns=cols_to_keep)
  senateDistricstData = senateDistricstData.rename(columns=cols_to_keep)
  congressionalDistrictsData = congressionalDistrictsData.rename(columns=cols_to_keep)
  tractsData = tractsData.rename(columns=cols_to_keep)
  zipData = zipData.rename(columns=cols_to_keep)
  # convert cols to numeric except FIPS
  # try, skip fails
  for data in [countyData, assemblyDistrictData, senateDistricstData, congressionalDistrictsData, tractsData, zipData]:
    for col in data.columns:
      if col != 'FIPS':
        try:
          data[col] = pd.to_numeric(data[col])
        except:
          pass
  congressionalDistrictsData['FIPS'] = congressionalDistrictsData['FIPS'].astype(str).str.slice(-1)
  assemblyDistrictData['FIPS'] = assemblyDistrictData['FIPS'].astype(str).str.slice(2,).astype(int).astype(str)
  senateDistricstData['FIPS'] = senateDistricstData['FIPS'].astype(str).str.slice(2,).astype(int).astype(str)
  
  countyData.to_parquet(os.path.join(data_dir, 'output', "countyData.parquet"))
  assemblyDistrictData.to_parquet(os.path.join(data_dir, 'output', "assemblyDistrictData.parquet"))
  senateDistricstData.to_parquet(os.path.join(data_dir, 'output', "senateDistricstData.parquet"))
  congressionalDistrictsData.to_parquet(os.path.join(data_dir, 'output', "congressionalDistrictsData.parquet"))
  tractsData.to_parquet(os.path.join(data_dir, 'output', "tractsData.parquet"))
  zipData.to_parquet(os.path.join(data_dir, 'output', "zipData.parquet"))

if __name__ == "__main__":
  data_dir = os.path.join(os.getcwd(), "data")
  handle_community_vars(data_dir)