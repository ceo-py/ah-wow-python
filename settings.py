from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())


WOW_DIRECTORY = CONFIG["WOW_DIRECTORY"]
REGION = "eu"

FILE_NAME = "merged_filtered_auctions.json"
MERGE_JSON_LOCATION = r"D:\VSC\ah-wow-python\data\realms"

CLIENT_SECRET = CONFIG["CLIENT_SECRET"]
CLIENT_ID = CONFIG["CLIENT_ID"]

REQUESTS_PER_HOUR = CONFIG["REQUESTS_PER_HOUR"]
REQUESTS_PER_SECOND = CONFIG["REQUESTS_PER_SECOND"]

BATTLE_NET_AUTH_URL = "https://oauth.battle.net/token"
