import pandas as pd
import subprocess
import os

class DataLoader():

    def load_set_price_guide(self, data_directory, set_id="75902-1",  exclude_incomplete=True):
        path = os.path.join(f"{data_directory}/SETS/{set_id}-{'C' if exclude_incomplete else 'CI'}")
        url = f"https://www.bricklink.com/catalogPG.asp?S={set_id}&colorID=0&v=D&viewExclude={'Y' if exclude_incomplete else 'N'}&cID=Y"
        data = self._get_price_guide_data(path, url)
        price_guide = self._parse_data(data)
        return price_guide

    # wasnt downloading right, skipping for now
    #def load_part_price_guide(self, data_directory="/DATA", part_id='21042pb01c02', color_id='150'):
    #    path = os.path.join(f"{data_directory}/PARTS/{part_id}-{color_id}")
    #    url = f"https://www.bricklink.com/catalogPG.asp?P={part_id}&ColorID={color_id}"
    #   url = "https://www.bricklink.com/catalogPG.asp?P=21042pb01c02&colorID=150&viewExclude=N&v=D&Y"
     #   return self._get_price_guide_data(path, url)

    def _get_price_guide_data(self, path, url):
        """
        manages storage / pulling of price guide data
        @param url: url of bricklink price guide of item
        @param path: relative path to where data is stored / will be stored 
        """
        if not os.path.exists(path):
            _status, output = subprocess.getstatusoutput(f"curl {url}")
            with open(path, "w+") as file:
                file.write(output)
            
        with open(path, "r") as file:
            data = file.read()

        return data

    def _parse_data(self, data):
        """
        parses raw data into dataframes
        @param data: downloaded html of price guide page
        @returns history, book
        """

        df = pd.read_html(data)

        #for table, i in enumerate(df):
        #    print(f"{i}.................................: \n\n{table}\n")

        if (len(df[19:-7]) % 3):
            print("\n\nBAD DATA!!!\n\n")
            
        history = pd.DataFrame()
        min_date = pd.Timestamp.today()
        new = True
        for i, item in enumerate(df[19:-7]):
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
        history = history.astype({'Qty': 'int', 'Each': 'string'})
        history['Each'] = history['Each'].apply(lambda x: x[x.find("$")+1:])
        history = history.astype({'Each': 'float'})
        history = history.sort_values(by='Date')

        book = pd.DataFrame()
        for i, item in enumerate(df[-7:-1]):
            new = i % 6 == 2
            if i % 3 == 2:
                item.columns = item.iloc[0]
                item = item.iloc[1:-7,1:]
                item['New'] = [new for x in item.index]
                book = pd.concat((book, item))

        return (history, book)

def main():
    data_loader = DataLoader()
    print(data_loader.load_set_price_guide(os.path.dirname(__file__)+"/DATA"))
    #print(data_loader.load_part_price_guide())

if (__name__ == '__main__'):
    main()