import requests
import json
import pandas as pd
import time
import random
from datetime import date
import argparse

appID = '730' # 730 for CS:GO
currency = '3' # 3 for EURo
market_link_prefix = f'https://steamcommunity.com/market/listings/{appID}/'


def get_price_for(item_name:str):
    url = f'http://steamcommunity.com/market/priceoverview/?appid={appID}&market_hash_name={item_name}&currency={currency}'
    response = requests.get(url)

    sleep_time = random.random() * 5 + 5
    time.sleep(sleep_time)

    if response.status_code == 200:
        data = json.loads(response.text)
        # print(data)
        price = data['lowest_price']
        print(f'The current price of {item_name} in Euros is {price}.')
        return price
    else:
        print(f'Request failed with status code {response.status_code}')
        if response.status_code == 429:
            sleep_time = random.random() * 60 + 60
            print(f"Waiting for {sleep_time} seconds because of error 429 (Too Many Requests)")
            print("Trying again later...")
            time.sleep(sleep_time)
            return get_price_for(item_name)
        else:
            return None


def read_file(file_name='prices.xlsx'):
    print(f'Table is read from {input_file}.')
    df = pd.read_excel(file_name)
    return df

def write_file(df, file_name='new_prices.xlsx'):
    print()
    print(f'Saving table with new prices as {output_file}.')
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer, index=False)
    writer._save()

def update_prices(df, item_column='Items', prices_column='New Prices'):
    print()
    print(f'Using {item_column} as column for item names.')
    print(f'New prices will be written to column "{prices_column}"')
    print('This programm is using random sleep times to prevent Error 429 (Too Many Requests).')
    print()
    for index, row in df.iterrows():                                    # for every item in the list:
        # print(f'Checking item #{index}')
        item_name = row[item_column]                                    # get the name of the item to search for the price
        current_price = get_price_for(item_name)                        # crawl price for item from community market
        if current_price:
            current_price = convert_to_number(current_price)            # convert price into a float for excel number representation
            df.at[index, prices_column] = current_price                 # write price of the item to the new column
        else:
            print(f"Couldn't find prices for {item_name}. Using 0€ instead.")
            df.at[index, prices_column] = 0
            print('Continuing with the next item...')
        if index % 20 == 0:
            sleep_time = random.random() * 5 + 5
            time.sleep(sleep_time)

def convert_to_number(price:str):
    result = price[:-1]                 # cut of the €-sign at the end
    result = result.replace("--", "00") # replace "--" with "00" in case it's a smooth euro amount
    result = result.replace(" ", "")    # remove empty spaces in the middle if the price is over 1000€
    result = result.replace(",", ".")   # replace the comma with a dot to be able to make it a float
    return float(result)                # return the result as a float


def clean_up_item_names(df, item_column='Items'): 
    for index, row in df.iterrows():                # for every item in the list:
        item_name = row[item_column]                # get name of the item
        item_name = item_name.replace("%20", " ")   # replace all encoded spaces with actual spaces
        item_name = item_name.replace("%7C", "|")   # replace all encoded | with actual |
        item_name = item_name.replace("%28", "(")   # replace all encoded ( with actual (
        item_name = item_name.replace("%29", ")")   # replace all encoded ) with actual )
        df.at[index, item_column] = item_name       # write new item name to table

def create_market_links(df, item_column='Items', link_column='Market Link'):
    for index, row in df.iterrows():                                # for every item in the list:
        market_hash_name = row[item_column]                         # get name of the item
        market_hash_name = market_hash_name.replace(" ", "%20")     # replace every space with encoded spaces
        market_hash_name = market_hash_name.replace("|", "%7C")     # replace every | with encoded |
        market_link = market_link_prefix + market_hash_name         # build actual market link
        df.at[index, link_column] = market_link                     # write market link to table

def get_price_column_name_with_date():
    today = date.today()
    formatted_date = today.strftime("%d.%m.%Y")
    print("Today's date:", formatted_date)
    column_name = f'Prices ({formatted_date})'
    return column_name

def main(input_file, output_file, item_column):
    df = read_file(input_file)
    prices_column = get_price_column_name_with_date()
    clean_up_item_names(df, item_column=item_column)
    create_market_links(df, item_column=item_column)
    update_prices(df, item_column=item_column, prices_column=prices_column)
    write_file(df, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program helps to crawl item prices from the community market, secifically items from the game "Counter-Strike: Global Offensive"')

    # Add the arguments
    parser.add_argument('-if', '--input_file', type=str, help='Name of the input file, e.g. example.xlsx. Default is prices.xlsx.', default="prices.xlsx")
    parser.add_argument('-of', '--output_file', type=str, help='Name of the output file, e.g. example.xlsx. Default is new_prices.xlsx. You can also use the same input as output file. This might however destroy some Excel specific functions and is therefore not recommended if you rely on that.', default="new_prices.xlsx")
    parser.add_argument('-i', '--item_column', type=str, help='Name of the column to crawl the item names from. Default is "Items".', default="Items")

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    input_file = args.input_file
    output_file = args.output_file
    item_column = args.item_column

    main(input_file, output_file, item_column)