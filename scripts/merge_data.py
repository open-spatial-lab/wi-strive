# %%
import pandas as pd
import geopandas as gpd
# remove col limit
pd.set_option('display.max_columns', None)
# %%
lcc_data = pd.read_excel('../data/LCC Directory.xlsx')
# remove digits after dash in zip code
lcc_data['Zip Code'] = lcc_data['Zip Code'].str.split('-').str[0]
# group by Zip Code and Application Type	
lcc_data = lcc_data.groupby(['Zip Code', 'Application Type']).size().reset_index(name='counts')
# get row with zip code, application type, and count of applications
lcc_data = lcc_data.pivot(index='Zip Code', columns='Application Type', values='counts').reset_index().fillna(0)
lcc_data['Zip Code'] = lcc_data['Zip Code'].astype(int)
# %%
geo = pd.read_csv("../data/wi_zip.csv")
# %%
census_data = pd.read_csv("../data/R13395265_SL860.csv")
census_cols = [
    '5-digit ZIP Code Tabulation Area',
    'Total Population',
    'Total',
    'Average Commute to Work (In Min)'
]
census_data = census_data[census_cols]
census_data = census_data.rename(columns={
    '5-digit ZIP Code Tabulation Area': 'GEOID10',
    'Total Population': 'Population',
    'Total': 'Avg Age',
    'Average Commute to Work (In Min)': 'Avg Commute Time'
})
  # %%
geo = geo.merge(census_data, on='GEOID10')
geo = geo.merge(lcc_data, left_on='GEOID10', right_on='Zip Code', how='left')
# %%
geo = geo[~geo.WKT.str.contains('EMPTY')]
geo = geo.fillna(0)
# %%

geo.to_csv("../data/wi_zip_joined.csv", index=False)
# %%
