import pandas as pd
import os
import subprocess
from functools import reduce

def get_set_path(data_directory="../DATA", set_id="75902-1", exclude_incomplete=True):
    return os.path.join(os.path.dirname(__file__), f"{data_directory}/SETS/{set_id}{'C' if exclude_incomplete else 'CI'}")

def download_set_price_guide(data_directory="../DATA", set_id="75902-1", exclude_incomplete=True):
    """
    stores result of curl request
    params:
        data_directory: string, path from __file__ to DATA folder
        set_id: string form, including dashes (e.g. 75902-1)
        exclude_incomplete: bool, whether to include incomplete sets
    returns:
        void 
    """

    url = f"https://www.bricklink.com/catalogPG.asp?S={set_id}&colorID=0&v=D&viewExclude={'Y' if exclude_incomplete else 'N'}&cID=Y"
    path = get_set_path(data_directory, set_id, exclude_incomplete)
    _status, output = subprocess.getstatusoutput(f"curl {url}")
    with open(path, "w+") as file:
        file.write(output)
    
def download_set_price_guide():

    f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={part_number}&idColor={page_color}#T=P&C={price_and_quantity_color}"


def load_set_dataframes(data_directory="../DATA", set_id="75902-1", exclude_incomplete=True):
    """
    params:
        data_directory: string, path from __file__ to DATA folder
        set_id: string form, including dashes (e.g. 75902-1)
        exclude_incomplete: bool, whether to include incomplete sets
    returns:
        void 
    """
    path = get_set_path(data_directory, set_id, exclude_incomplete)
    with open(path, "r") as file:
        tables = pd.read_html(file.read())

    discard = tables[:11]
    summaries = tables[11:19]
    months = tables[19:-7]
    book = tables[-7:-1]
    discard = tables[-1:]

    if (len(months) % 3):
        print("\n\nBAD DATA!!!\n\n")

    column_names = {1:'6M_NEW', 3:'6M_USED', 5:'BOOK_NEW', 7:'BOOK_USED'}
    cleaned_summaries = [summaries[i].set_index(0).rename(columns={1: column_names[i]}) for i in {1, 3, 5, 7}]
    summary = reduce(lambda  left,right: pd.merge(left,right, left_index=True, right_index=True), cleaned_summaries)
    summary = summary.transpose()
    
    print(summary)

def main():
    load_set_dataframes()
    pass

if (__name__ == '__main__'):
    main()