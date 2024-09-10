# World of Warcraft Auction House Data Scraper

## Project Overview

This project is designed to collect and analyze auction house data from all realms in World of Warcraft (WoW). The script retrieves auction house posts from each realm, processes the data, and saves it in JSON files. As of the creation of this script, there are **266 realms** on the EU servers, with the total auction house data amounting to approximately **7 GB**.

## Features

- **Data Collection**: Fetches auction house data for all realms.
- **Data Storage**: Saves the auction house data into JSON files.
- **Data Querying**: Allows searching for specific items by their ID to find the minimum price across all realms.

## Usage

1. **Setup and Configuration**:
   - Ensure you have the correct API credentials and configuration by setting up the `.env` file. This file should include your API key and any other required configurations for making requests to the Battle.net API and retrieving realm information.

2. **Run Data Collection**:
   - Before running queries, you need to collect or update the data. Run the `get_data()` function to fetch and save the auction house data from all realms. This should be done:
     - **Initially**: The first time you start the script.
     - **Periodically**: To refresh the data as Blizzard updates auction house information approximately every 15-30 minutes.

3. **Function to Search for Items**:
   - After collecting data, you can search for a specific item using the following function:
     ```python
     show_data_for_item(item_id: int, file_name: str) -> None
     ```
   - Replace `item_id` with the ID of the item you are looking for and `file_name` with the path to your JSON file containing the auction house data.

4. **Output**:
   - The function will display information about each realm with the minimum price for the specified item. Additionally, if you have a character in any of those realms, it will be indicated with an `X`.

## Example
![Example Output](https://github.com/ceo-py/ah-wow-python/blob/main/example_picture/example.png?raw=true)

## Notes

- **Data Collection**: Make sure to run `get_data()` whenever you start the script for the first time or when you want to update the data. This ensures you are working with the latest auction house information.
- **Data Updates**: Blizzard updates auction house data approximately every 15-30 minutes. To keep your data current, consider running `get_data()` at regular intervals.

## Prerequisites

- **Required Libraries**: Ensure you have the necessary Python libraries installed. You can install them using:
  ```bash
  pip install -r requirements.txt
  ```
