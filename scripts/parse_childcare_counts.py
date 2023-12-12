# %%
import pandas as pd
import os
# %%
def update_childcare_counts(path_to_childcare: str):
  data = pd.read_excel(path_to_childcare)
  data = data.fillna(method='ffill')
  data = data[data["Funding Period"].str.contains('-')]
  
  # clean up payment amount
  data['Payment Amount'] = data['Payment Amount'].str.replace('$', '').replace(',', '', regex=True).astype(float)

  # split funding period on -
  # make date
  # as datetyime mm/dd/yyyy
  data['Start Date'] = data['Funding Period'].apply(lambda x: x.split('-')[0])
  data['Start Date'] = pd.to_datetime(data['Start Date'], format='mixed')
  data["Provider Number"] = data["Provider Location Number"].apply(lambda x: x.split(' ')[0])
  data['Location Number'] = data['Provider Location Number'].apply(lambda x: x.split(' ')[1])
  data['monthyear'] = data['Start Date'].dt.strftime('%Y-%m')
  return data

if __name__ == '__main__':
  filepath = os.path.join(os.getcwd(), 'data', 'wi_childcare_counts','childcare_counts.xlsx')
  df = update_childcare_counts(filepath)
  today = pd.to_datetime('today').strftime('%Y-%m')
  df.to_parquet(os.path.join(os.getcwd(), 'data', 'output',f'childcare_counts_{today}.parquet'), index=False)
  df.to_csv(os.path.join(os.getcwd(), 'data', 'output',f'childcare_counts_{today}.csv'), index=False)