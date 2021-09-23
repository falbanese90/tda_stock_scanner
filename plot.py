import matplotlib.pyplot as plt

def plot(dataframe, title):
    plt.figure(figsize=[16, 8])
    plt.plot(dataframe['close'], label=title)
    plt.plot(dataframe['MA10'], label='MA10')
    plt.plot(dataframe['MA20'], label='MA20')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.legend()
    plt.savefig(f'{title}.png')
    plt.show()
    