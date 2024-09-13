import os
import json
import pandas as pd
from settings import MERGE_JSON_LOCATION, FILE_NAME


def process_file_to_dataframe(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as file:
        data = json.loads(file.read())
        auctions_data = data.get("auctions", [])
        if not auctions_data:
            return

        auctions_df = pd.json_normalize(auctions_data)

        auctions_df = auctions_df[["item.id", "buyout"]]
        auctions_df = auctions_df.loc[auctions_df.groupby("item.id")["buyout"].idxmin()]
        realm_name = (
            file_path.replace(MERGE_JSON_LOCATION, "")
            .replace(".json", "")
            .replace("\\", "")
        )
        print(f"Realm Name => {realm_name}")
        auctions_df["realm"] = realm_name

        return auctions_df


def process_json_files_with_pandas(json_dir: str) -> pd.DataFrame:
    json_files = [
        os.path.join(json_dir, file)
        for file in os.listdir(json_dir)
        if file.endswith(".json")
    ]

    df_list = []

    for file_number, file_path in enumerate(json_files, 1):
        print(f"Realm Number => {file_number}")
        try:
            df = process_file_to_dataframe(file_path)
        except:
            print("error")
            continue
        print(f"Finished file => {file_path}\n")
        df_list.append(df)

    merged_df = pd.concat(df_list, ignore_index=True)

    merged_df.dropna(subset=["item.id", "buyout"], inplace=True)

    return merged_df


def load_data():
    json_dir = MERGE_JSON_LOCATION

    lowest_buyout_df = process_json_files_with_pandas(json_dir)

    lowest_buyout_df.to_json(FILE_NAME, orient="records", indent=4)

    print(f"Processing complete. Results saved to '{FILE_NAME}'.")


# # load_data()
