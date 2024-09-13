from realms.get_all_connected_realms import (
    get_all_connected_realms,
    ConnectedRealmsResponse,
)
from realms.get_connected_realm import get_connected_realm
from action_house.get_ah_posts import get_ah_posts, get_ah_posts_multi
from settings import (
    WOW_DIRECTORY,
    REGION,
    FILE_NAME,
    BATTLE_NET_AUTH_URL,
    CLIENT_ID,
    CLIENT_SECRET,
)
from create_file.create_json_file import create_json_file
from compere.compere_item import extract_buyout_prices
from merge_data_into_json import load_data
from character.get_realms_with_character import get_realms_with_character
from auth.generate_token import get_battle_net_token
import json
import pandas as pd
import asyncio


ACCESS_TOKEN = get_battle_net_token(CLIENT_ID, CLIENT_SECRET, BATTLE_NET_AUTH_URL)


async def connected_realms(region: str, token: str):
    return await get_all_connected_realms(region, token)


async def show_connected_realm(all_connected_realms: ConnectedRealmsResponse):

    total = 0
    for connected_realm in all_connected_realms.connected_realms:
        try:
            connected_realm_response = await get_connected_realm(
                REGION, connected_realm.href, ACCESS_TOKEN
            )
        except Exception as e:
            continue

        for realm in connected_realm_response.realms:
            response = await get_ah_posts(
                REGION, realm["connected_realm"]["href"], ACCESS_TOKEN
            )
            file_name_creation = (
                f"{realm['slug']}-{connected_realm_response.population.get('type')}"
            )
            create_json_file(file_name_creation, response)
            print(realm["slug"])
            total += 1
            print(total)


async def show_connected_realm_multi(all_connected_realms: ConnectedRealmsResponse):
    tasks = []
    for connected_realm in all_connected_realms.connected_realms:

        try:
            connected_realm_response = await get_connected_realm(
                REGION, connected_realm.href, ACCESS_TOKEN
            )
        except Exception as e:
            continue

        for realm in connected_realm_response.realms:
            tasks.append((REGION, realm["connected_realm"]["href"]))

        response = await get_ah_posts_multi(tasks, ACCESS_TOKEN)

    for num_, data in enumerate(response):
        create_json_file(f"{num_}", data)


# Run the async function


def get_data():
    try:
        connected_realms_response = asyncio.run(connected_realms(REGION, ACCESS_TOKEN))

        asyncio.run(show_connected_realm(connected_realms_response))
        load_data()

        # asyncio.run(show_connected_realm_multi(connected_realms_response))
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise


def show_data_for_item_single(id: int):
    data = asyncio.run(extract_buyout_prices(id))
    min_prices = {item: min(prices) for item, prices in data.items()}
    sorted_diff = sorted(min_prices.items(), key=lambda x: x[1], reverse=True)

    for realm, price in sorted_diff:
        print(f"Realm: {realm[:realm.index('.')].upper()}, Price: {price / 10000:.2f}")


def show_data_for_item(id: int, file_name: str) -> None:
    with open(file_name, "r") as file:
        data = json.load(file)

    auctions_df = pd.json_normalize(data)

    df = pd.DataFrame(auctions_df)

    df_filtered = df[df["item.id"] == id]

    if df_filtered.empty:
        print(f"No data found for item ID {id}.")
        return

    realms_with_characters = get_realms_with_character(WOW_DIRECTORY)
    print(realms_with_characters)
    df_filtered["buyout"] = df_filtered["buyout"] / 10000
    df_sorted = df_filtered.sort_values(by="buyout")
    df_sorted["Character"] = df_sorted["realm"].apply(
        lambda x: "X" if any(realm in x for realm in realms_with_characters) else ""
    )

    pd.set_option("display.max_rows", None)  # Show all rows
    pd.set_option("display.max_columns", None)  # Show all columns
    pd.set_option("display.width", None)  # Do not truncate the display width
    pd.set_option("display.max_colwidth", None)

    print(df_sorted)


get_data()

# regen
# show_data_for_item(222854, FILE_NAME)

# show_data_for_item(224592, FILE_NAME)
# show_data_for_item(220774, FILE_NAME)
# bag
# show_data_for_item(222856, FILE_NAME)


show_data_for_item(225721, FILE_NAME)


# show_data_for_item_single(222856)
