# CSGO-Market-Helper
This repository aims to help with crawling prices for CS:GO items from the Steam Community Market

## Setup
1. Clone the repository to your local machine or download project as a .zip and extract it.
2. Open the folder in your Windows Explorer and press right mouse click while holding `Shift`, then select `Open PowerShell window here` to enter Windows PowerShell
3. Run command `python3.exe` to install Python 3 from the Microsoft Store
4. Run command `pip3.exe install -r requirements.txt` to install the requirements for the script

``` bash
python3.exe
pip3 install -r requirements.txt
```

## Usage
You can run the script by using the command `python3.exe .\update_prices.py`.
You can see the documentation for additional arguments to change the input and output file or to specify the column with the item names by using `python3.exe .\update_prices.py --help`.

``` bash
python3 .\update_prices.py
```

The list of items needs to be a column in the input file `prices.xlsx`.
The item names need to match the correct hash names on the community market. You can retrieve these names by opening the item on the community market and copying the last part of the link where the name of the item is.

Example:
The link to the community market for the [AK-47 | Redline (Minimal Wear)](https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Minimal%20Wear%29) is `https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Minimal%20Wear%29`.
To get the hash name of the item you take everything after the `730/`, so you can use `AK-47%20%7C%20Redline%20%28Minimal%20Wear%29` as the item name in your excel spreadsheet.
However, using `AK-47 | Redline (Minimal Wear)` would work as well, it is just easier to only copy the links without manipulating the names when creating the list for the first time.
The script automatically 'cleans' the names to remove the `%20` and replaces it with blank spaces etc. to make it more readable.
You can see an example list for some items in [prices.xlsx](prices.xlsx).
