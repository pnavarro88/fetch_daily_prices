import pandas as pd
import numpy as np
import pandas.io.data as web
import datetime

names = ['AAPL', 'YHOO', 'GOOG', 'MSFT', 'AMZN', 'GLD', 'SLV', 'USO', 'SPY', 'XOM',
         'JPM', 'TLT', 'DIS', '^DJI', '^GSPC']
path = '/Users/Pablo/Documents/Stocks_Data/'
for name in names:
    print 'Downloading ', name
    today = datetime.date.today()
    today = ("%s/%s/%s" % (today.day, today.month, today.year))

    data = web.DataReader(name, data_source='yahoo',
                          start= '1/1/2008', end = 'today')
    del data['Adj Close']
    #del data['Close']
    #data['Close'] = data['Adj Close']
    data['PCT_Move'] = np.round((((data.Close - data.Close.shift(1))/ data.Close.shift(1)) * 100),2)
    data['Daily_Range'] = np.round((data.High - data.Low),2)
    data['Daily_Range_PCT'] = np.round((data.Daily_Range/data.Close)*100,2)
    data['ON_Gap'] = np.round((data.Open - data.Close.shift(1)),2)
    data['ON_Gap_PCT'] = np.round((data.ON_Gap/data.Close.shift(1))*100,2) 
    data['Gap_Filled'] = False
    data['Gap_Trend'] = False # means that it closes +/- if it opened +/- 
    data['Up_Down_Day'] = 'NaN'
    data.to_csv(name+'.csv')
    print 'Done with ', name
#Adding Gap and T+/- Days Data

for name in names:
    data = pd.read_csv(name+'.csv')
    for key in data.Close.keys():
        if key == 0:
            continue
        elif data.Close[key] > data.Close[key-1]:
            data.Up_Down_Day[key] = 1
        elif data.Close[key] < data.Close[key-1]:
            data.Up_Down_Day[key] = -1
        elif data.Close[key] == data.Close[key-1]:
            data.Up_Down_Day[key] = 0
        if data.ON_Gap[key] > 0.0:
            if data.Low[key] < data.Close[key-1]:
                data.Gap_Filled[key] = True
            if data.Close[key] > data.Close[key-1]:
               data.Gap_Trend[key] = True
        if data.ON_Gap[key] < 0.0:
            if data.High[key] > data.Close[key-1]:
                data.Gap_Filled[key] = True
            if data.Close[key] < data.Close[key-1]:
                data.Gap_Trend[key] = True
    
    data['5_Day_Return'] = np.round(((data['Close'] - data['Close'].shift(5)) / 
                             data['Close'].shift(5)) *100,2)
    data['10_Day_Return'] = np.round(((data['Close'] - data['Close'].shift(10)) / 
                             data['Close'].shift(10)) *100,2)
    data['20_Day_Return'] = np.round(((data['Close'] - data['Close'].shift(20)) / 
                             data['Close'].shift(20)) *100,2)
    data['1_day_Future_Return'] = np.round(((data['Close'].shift(-1) - data['Close']) / 
                             data['Close']) *100,2)
    data['5_Day_Future_Return'] = np.round(((data['Close'].shift(-5) - data['Close']) / 
                             data['Close']) *100,2)
    data['10_Day_Future_Return'] = np.round(((data['Close'].shift(-10) - data['Close']) / 
                             data['Close']) *100,2)
    data['20_Day_Future_Return'] = np.round(((data['Close'].shift(-20) - data['Close']) / 
                             data['Close']) *100,2)
    
    data.to_csv(path+name+'.csv')
    