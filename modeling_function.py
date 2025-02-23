import pandas as pd
pd.set_option('display.max_rows', None)
metro_bike = pd.read_csv("raw_data/Austin_MetroBike_Trips_20250221.csv", encoding="latin1")
kiosk_info = pd.read_csv("raw_data/Austin_MetroBike_Kiosk_Locations_20250221.csv", encoding="latin1")

# rename column names
# df.rename(columns={"A": "Column1", "B": "Column2"}, inplace=True)
metro_bike.rename(columns = {"Trip ID": "trip_id", "Membership or Pass Type": "pass_type",
                             "Bicycle ID": "bike_id", "Bike Type": "bike_type", 
                             "Checkout Datetime": "checkout_datetime", "Checkout Date": "checkout_date",
                             "Checkout Time": "checkout_time", "Checkout Kiosk ID": "checkout_kiosk_id",
                             "Checkout Kiosk": "checkout_kiosk", "Return Kiosk ID": "return_kiosk_id",
                             "Return Kiosk": "return_kiosk", "Trip Duration Minutes": "trip_duration_minutes",
                             "Month": "month", "Year": "year"}, inplace = True)
kiosk_info.rename(columns = {"Kiosk ID": "kiosk_id", "Kiosk Name": "kiosk_name", "Kiosk Status": "kiosk_status",
                             "Location": "location", "Address": "address", "Number of Docks": "number_of_docks"},
                             inplace = True)

# print(metro_bike[metro_bike["membership_type"] == "Founding Member"])
# year_2020 = metro_bike[metro_bike["year"] == 2020]
# print(year_2020.head())
# print(metro_bike.dtypes)

kiosk_list = metro_bike['checkout_kiosk_id'].unique().tolist()
kiosk_list_2 = kiosk_info['kiosk_id'].unique().tolist()
year_list = metro_bike['year'].unique().tolist()
def metro_bikedoc_usage(select_year, select_kiosk):
    if (select_kiosk in kiosk_list) and (select_kiosk in kiosk_list_2) and (select_year in year_list):
        checkout_kiosk_id= pd.to_numeric(metro_bike['checkout_kiosk_id'], errors='coerce').dropna()
        return_kiosk_id = pd.to_numeric(metro_bike['return_kiosk_id'], errors='coerce').dropna()
        data = metro_bike[(metro_bike["year"] == select_year) & 
                        ((checkout_kiosk_id == select_kiosk) | (return_kiosk_id == select_kiosk))]
        if not data.empty:
            # print(f"Query data info: {data.shape}")
            data = data.sort_values('checkout_datetime', ascending= True)
            # print(data[['year', 'return_kiosk_id', 'checkout_kiosk_id', 'trip_duration_minutes', 'checkout_datetime']].iloc[:10])
            locate_kiosk = kiosk_info[kiosk_info['kiosk_id'] == select_kiosk]
            num_of_doc = locate_kiosk['number_of_docks'].iloc[0]
            #create two different type of rows and combine them into one dataframe
            checkout_rows = pd.DataFrame({"action": "checkout",
                                            "kiosk_id": data['checkout_kiosk_id'],
                                            "time": pd.to_datetime(data['checkout_datetime'])})
            return_rows = pd.DataFrame({"action": "return",
                                        "kiosk_id": data['return_kiosk_id'],
                                        "time": pd.to_datetime(data['checkout_datetime']) + pd.to_timedelta(data['trip_duration_minutes'], unit = "m")})
            transaction_data = pd.concat([return_rows, checkout_rows]).sort_values('time', ascending= True)

            unique_id_list = []
            k = 0
            for i in range(len(transaction_data)):
                unique_id_list.append(k)
                k = k + 1
            transaction_data['unique_id'] = unique_id_list
            # print(transaction_data.iloc[:10])

            kiosk_full_times = 0
            doc_count = num_of_doc
            transaction_list = transaction_data['unique_id'].tolist()
            for i in transaction_list:
                current_transaction = transaction_data[transaction_data['unique_id'] == i]
                if current_transaction['kiosk_id'].iloc[0] == select_kiosk:
                    if current_transaction['action'].iloc[0] == 'checkout':
                        doc_count -= 1
                    else:
                        doc_count += 1
                if doc_count == num_of_doc:
                    kiosk_full_times += 1
            return kiosk_full_times
        else:
            return None
    else:
        return None
    
full_count_df = pd.DataFrame({"id": [], "kiosk": [], "year": [], "full_times": []})
key_id = 0
for i in kiosk_list_2:
    for j in year_list:
        full_times = metro_bikedoc_usage(j, i)
        full_count_df.loc[len(full_count_df)] = [key_id, i, j, full_times]
        key_id += 1
        print(key_id)
        

print(full_count_df.iloc[:10])
full_count_df.to_csv("full_count_df.csv")
    


