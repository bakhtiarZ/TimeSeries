import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
data = pd.read_csv('../data/data.csv')


def plotter():
    timedf = data['Time'][20:60]
    signaldf = data['signal'][20:60]
    ds_dt = signaldf.diff()
    ds_dt_abs = ds_dt.abs()
    d2s_dt2 = ds_dt_abs.diff()
    d2s_dt2_abs = d2s_dt2.abs()
    # plt.plot(timedf, signaldf, label='signal')
    plt.plot(timedf, d2s_dt2_abs, label='d2_s_dt2')
    for x in data['Trade Timestamps'][1:30]:
        plt.axvline(x=x, color='red', linestyle='--', linewidth=0.2)
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.tight_layout()
    plt.show()

# Press the green button in the gutter to run the script.
def myownattempt():
    df = data
    trade_timestamps = df['Trade Timestamps']
    time = df['Time']
    signal = df['signal']
    filtered_data = pd.DataFrame()
    for i, trade_timestamp in enumerate(trade_timestamps):
        param = df.iloc[(df['Time'] - df['Trade Timestamps'][i]).abs().argsort()[:1]]
        if param.index < 1000:
            param['Trade Timestamps'] = trade_timestamp
            param['center'] = True;
            if param.index != 0:
                tmp = df.iloc[param.index - 1]
                tmp['Trade Timestamps'] = trade_timestamp
                tmp['center'] = False
                filtered_data = pd.concat([filtered_data, tmp])
            filtered_data = pd.concat([filtered_data, param])
            if param.index != 0:
                tmp = df.iloc[param.index + 1]
                tmp['Trade Timestamps'] = trade_timestamp
                tmp['center'] = False
                filtered_data = pd.concat([filtered_data, tmp])

    differences = []
    timestamps = []
    skiprow = True
    for i, item in filtered_data.iterrows():
        if item.loc['center'] == True and not skiprow:
            term1 = filtered_data.at[i-1, 'signal']
            term2 = filtered_data.at[i + 1, 'signal']
            if(isinstance(term1,pd.Series)):
                term1 = term1.iloc[0]
            if (isinstance(term2, pd.Series)):
                term2 = term2.iloc[0]
            timestamp = item.at['Time']
            timestamps.append(timestamp)
            difference = abs(term1 - item.at['signal']) + abs(term2 - item.at['signal'])
            differences.append(difference/item.at['signal'])#need to add relative difference

        skiprow = False
    finaldf = pd.DataFrame({"differences" : differences, "timestamps" : timestamps})
    finaldf = finaldf.drop_duplicates(subset=['timestamps'], keep='first')
    print(finaldf)
    finaldf = finaldf[finaldf['differences'] < 5]
    finaldf.plot(x="timestamps", y="differences", kind="line")
    plt.show()

    # plt.figure(figsize=(10, 5))
    # plt.hist(finaldf['differences'], bins=100, density=True, alpha=0.6, color='g')
    # plt.xlabel('differences')
    # plt.ylabel('frequency density')
    # plt.title('Histogram of differences')
    # plt.show()

if __name__ == '__main__':
    myownattempt()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
