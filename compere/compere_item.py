import aiofiles
import json
import os

async def load_json_file(file_path):
    async with aiofiles.open(file_path, 'r') as file:
        content = await file.read()
        return json.loads(content)

async def extract_buyout_prices(item_id):
    starting_directory = os.getcwd()
    directory = os.path.join(starting_directory, 'data', 'realms')
    print(directory)
    buyout_prices = {}

    for file_name in os.listdir(directory):
        if not file_name.endswith('.json'):
            continue

        file_path = os.path.join(directory, file_name)
        data = await load_json_file(file_path)
        auctions = data.get('auctions', [])
        for auction in auctions:
            if auction['item']['id'] == item_id:
                buyout_prices[file_name] = buyout_prices.get(file_name, []) + [auction['buyout']]

    return buyout_prices
