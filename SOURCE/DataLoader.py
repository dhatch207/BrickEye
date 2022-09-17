from operator import irshift
from time import time
from typing import *
from numpy import piecewise
import pandas as pd
import os
import subprocess
from functools import reduce
from os.path import exists

class DataLoader():

    def load_set_price_guide(self, data_directory="../DATA", set_id="75902-1",  exclude_incomplete=True):
        path = os.path.join(os.path.dirname(__file__), f"{data_directory}/SETS/{set_id}{'C' if exclude_incomplete else 'CI'}")
        url = f"https://www.bricklink.com/catalogPG.asp?S={set_id}&colorID=0&v=D&viewExclude={'Y' if exclude_incomplete else 'N'}&cID=Y"
        return self._get_price_guide_data(path, url)

    def load_part_price_guide(self, data_directory="../DATA",part_number='62113',page_color='11',price_and_quantity_color='85'):
        path = os.path.join(os.path.dirname(__file__), f"{data_directory}/PARTS/{part_number}{price_and_quantity_color}")
        url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={part_number}&idColor={page_color}#T=P&C={price_and_quantity_color}"
        return self._get_price_guide_data(path, url)

    def _get_price_guide_data(self, path, url):
        """
        manages storage / pulling of price guide data
        @param url: url of bricklink price guide of item
        @param path: relative path to where data is stored / will be stored 
        """
        if not exists(path):
            _status, output = subprocess.getstatusoutput(f"curl {url}")
            with open(path, "w+") as file:
                file.write(output)
            
        with open(path, "r") as file:
            data = pd.read_html(file.read())

        return self._parse_data(data)
        

    def _parse_data(self, data):
        """
        parses raw data into dataframes
        @param data: downloaded html of price guide page
        @returns history, book
        """

        if (len(data[19:-7]) % 3):
            print("\n\nBAD DATA!!!\n\n")
            
        history = pd.DataFrame()
        min_date = pd.Timestamp.today()
        new = True
        for i, item in enumerate(data[19:-7]):
            if i % 3 == 0:
                date = pd.to_datetime(item.iloc[0,0])
                if date > min_date:
                    new = False
                min_date = date
            if i % 3 == 2:
                item.columns = item.iloc[0]
                item = item.iloc[1:-7,1:]
                item['Date'] = [date for x in item.index]
                item['New'] = [new for x in item.index]
                history = pd.concat([history, item])

        book = pd.DataFrame()
        for i, item in enumerate(data[-7:-1]):
            new = i % 6 == 2
            if i % 3 == 2:
                item.columns = item.iloc[0]
                item = item.iloc[1:-7,1:]
                item['New'] = [new for x in item.index]
                print(item)
                book = pd.concat((book, item))

        return (history, book)

def main():
    data_loader = DataLoader()
    print(data_loader.load_set_price_guide())
    print(data_loader.load_part_price_guide())

if (__name__ == '__main__'):
    main()