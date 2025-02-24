import pandas as pd
pd.set_option('display.max_rows', None)
kiosks_full_counts = pd.read_csv('output_data/full_count_locations.csv', encoding = "latin1")

mean_groupby_kiosks = kiosks_full_counts.groupby('Kiosk ID').agg({'full_times': ['mean'], 'Kiosk Name': ['first']})
print(mean_groupby_kiosks.sort_values(('full_times', 'mean'), ascending = False))