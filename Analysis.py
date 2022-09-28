from numpy import size, mean
from DataLoader import DataLoader
import matplotlib.pyplot as plt

def plot_historical_transactions(history):
    df = history.copy()
    df = df.iloc[1:,:] # drop outlier
    df['color'] = df['New'].apply(lambda x: 'tab:blue' if x else 'tab:orange')
    
    plt.scatter(x=df['Date'], y=df['Each'], color=df['color'], s=df['Qty'] * 100)

    plt.show()

def get_average_six_month_sale_price(history):
    df = history.copy()
    df = df.iloc[1:,:] # drop outlier
    new = mean(df[df['New']]['Each'])
    used = mean(df[~df['New']]['Each'])
    return new, used


def main():
    data_loader = DataLoader()
    total_new, total_used = 0, 0
    #for set_id in ["10220-1", "75902-1", "75904-1", "10181-1"]:#, "5526-1"]:
    for set_id in ["75181-1", "75053-1", "75180-1", "7868-1", "7675-1", "7259-1", "8095-1",  "8096-1", "75176-1", "8098-1"]: #"4124171-1",
        history, book = data_loader.load_set_price_guide(set_id=set_id)
        #plot_historical_transactions(history)
        new, used = get_average_six_month_sale_price(history)
        total_new += new
        total_used += used
        print(f"set: {set_id} used: {used} new: {new}")
    print(f"total used: {total_used} new: {total_new}")
        

if (__name__ == '__main__'):
    main()