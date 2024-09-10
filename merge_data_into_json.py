import os
import json
import pandas as pd

# Function to process a single JSON file into a DataFrame
def process_file_to_dataframe(file_path):
    # Load the JSON data into a pandas DataFrame
    with open(file_path, 'r') as file:
        data = json.loads(file.read())
        # Normalize nested data into flat columns
        auctions_data = data.get('auctions', [])
        if not auctions_data:
            return

        auctions_df = pd.json_normalize(auctions_data)
        
        # Select only relevant columns: 'item.id', 'buyout'
        auctions_df = auctions_df[['item.id', 'buyout']]
        auctions_df = auctions_df.loc[auctions_df.groupby('item.id')['buyout'].idxmin()]
        realm_name = file_path.replace(r"D:\VSC\ah-wow-python\data\realms", '').replace(".json", '').replace("\\", "")
        print(f"Realm Name => {realm_name}")
        auctions_df["realm"] = realm_name
        
        return auctions_df

# Function to process and merge all JSON files
def process_json_files_with_pandas(json_dir):
    json_files = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if file.endswith('.json')]

    # Initialize an empty list to collect dataframes
    df_list = []

    # Iterate through each file and process it into a DataFrame
    for file_number, file_path in enumerate(json_files, 1):
        print(f"Realm Number => {file_number}")
        try:
            df = process_file_to_dataframe(file_path)
        except:
            print('error')
            continue
        print(f"Finished file => {file_path}\n")
        df_list.append(df)

    # Concatenate all DataFrames into one
    merged_df = pd.concat(df_list, ignore_index=True)

    # Drop rows where 'item.id' or 'buyout' is NaN
    merged_df.dropna(subset=['item.id', 'buyout'], inplace=True)


    return merged_df

def load_data():
        # Provide the correct path to your JSON files
        json_dir = r'D:\VSC\ah-wow-python\data\realms'
        
        # Process all JSON files and get the result DataFrame
        lowest_buyout_df = process_json_files_with_pandas(json_dir)
        
        # Save the DataFrame to a JSON file
        lowest_buyout_df.to_json('merged_filtered_auctions.json', orient='records', indent=4)
        
        print("Processing complete. Results saved to 'merged_filtered_auctions.json'.")

# load_data()