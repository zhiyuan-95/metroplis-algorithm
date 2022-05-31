import pandas_datareader as web
import pandas as pd
import numpy as np
import math
import random
from matplotlib import pyplot
import time
def get_stocks(tickers,start,end):
    for x in tickers:
        df = web.DataReader(x, data_source='yahoo', start='{0}-1-1'.format(start), end='{0}-12-31'.format(end))
        fileName = x+str(start)+str(end)
        df.to_csv(r"C:\Users\johnk\OneDrive\Desktop\project\data_store\{0}.csv".format(str(fileName)))
def Returns(tickers,Start,End):
    returns = []
    for i in tickers:
        SumReturn = 0
        df= web.DataReader(i, data_source='yahoo', start='{0}-1-1'.format(Start), end='{0}-12-31'.format(End))['Close']
        start = '1000'
        firstDayPrice,lastDayPrice,yesterday = 0,0,0
        totalReturn = 0
        lastdata = df.index[-1]
        for x in df.index:
            year = str(x)[0:4]
            if year!=start:
                n = 0
                start = year
                if yesterday == 0:
                    firstDayPrice = df.loc[x]
                else:
                    lastDayPrice = df.loc[yesterday]
                    returnThisYear = (lastDayPrice-firstDayPrice)/firstDayPrice
                    totalReturn += returnThisYear
                    firstDayPrice = df.loc[x]
            if x==lastdata:
                lastDayPrice = df.loc[x]
                current_return = (lastDayPrice-firstDayPrice)/firstDayPrice
                Average_return0 = totalReturn/(End-Start-1)
                returnThisYear = current_return*n/253+Average_return0*(253-n)/253
                totalReturn += returnThisYear
                Average_return = totalReturn/(End-Start)
                returns.append(Average_return)
            yesterday = x
            n+=1
    return returns
def correlation(tickers,start,end):
    df = pd.DataFrame()
    for x in tickers:
        fileName = x+str(start)+str(end)
        df1 = pd.read_csv(r"C:\Users\johnk\OneDrive\Desktop\project\data_store\{0}.csv".format(fileName))
        df[x]=df1['Close']
    C = df.corr()
    return C
t1 = 2020
t2 = 2022
Ticker = ['TQQQ','JD','BABA','LMT','DOG']
iter = len(Ticker)*20000
#['VTI','VOO','VYM','VTV','VNQ','VEA','VWO','BND','VCIT','MGC']

#['TQQQ','FXP','JD','BABA','DOG']
get_stocks(Ticker, t1, t2)
start_time = time.time()
number_of_stocks = len(Ticker)
C = correlation(Ticker,t1,t2)
m = Returns(Ticker,t1,t2)
w = np.array([round(1/len(Ticker),3) for x in Ticker])
OldEnerge = 100
T = 0.05
m = np.array(m)
risk = []
mu = []
rrMax = 0
RETURN = 0
RISK = 0
W = []
step = 0.01
for x in range(iter):
    i = random.randrange(0,number_of_stocks)
    j = i
    while i==j:
        j = random.randrange(0,number_of_stocks)
        if w[j]<0.001:
            j=i
    w[i]+=step
    w[j]-=step
    varience = np.dot(np.dot(w,C),w.T)
    std = math.sqrt(varience)

    r = np.dot(w,m.T)
    returnOverRisk = (r-0.004)/std
    NewEnerge = -returnOverRisk
    deltaEnerge = NewEnerge-OldEnerge
    if deltaEnerge<0:
        OldEnerge=NewEnerge
    else:
        b = random.uniform(0,1)
        if b<math.exp(-deltaEnerge/T):
            OldEnerge = NewEnerge
        else:
            w[j]+=step
            w[i]-=step
    if rrMax<returnOverRisk:
        rrMax = returnOverRisk
        RISK = std
        RETURN =r
        W = w
        risk.append(std)
        mu.append(r)
    if x%2000==0:
        if x%4000==0:
            print(x,(RETURN-0.004)/RISK)
        risk.append(std)
        mu.append(r)

print('weight: ',W)
for x in W:
    if x>0.05:
        id = W.tolist().index(x)
        print(Ticker[id],round(x,4))
print('risk_over_return: ',(RETURN-0.004)/RISK)
print(' expected return: ', RETURN)
print('             std: ', RISK)
print("--- %s seconds ---" % (time.time() - start_time))
pyplot.scatter(risk,mu,s=3)
pyplot.scatter(RISK,RETURN,color = 'red')
pyplot.xlabel('risk')
pyplot.ylabel('return')
pyplot.show()
print('python metro_ror.py')
