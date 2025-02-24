import pandas as pd
pd.set_option('display.max_rows', None)
kiosk_info = pd.read_csv("raw_data/Austin_MetroBike_Kiosk_Locations_20250221.csv", encoding="latin1")
full_count = pd.read_csv("output_data/full_count_df.csv", encoding="latin1")

kiosk_name = kiosk_info[['Kiosk ID', 'Kiosk Name']]
result = pd.merge(full_count, kiosk_name, how = 'left', left_on = ['kiosk'], right_on = ['Kiosk ID'])
data = result[['id', 'Kiosk ID', 'Kiosk Name', 'year', 'full_times']]
data['full_times'] = data['full_times'].fillna(0)
data.to_csv('output_data/full_count_locations.csv')


