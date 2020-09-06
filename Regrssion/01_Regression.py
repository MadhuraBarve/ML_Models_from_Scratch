## Importing the libraries
import numpy as np
import pandas as pd
import quandl as qd
import math, datetime
from sklearn import preprocessing, svm
# from sklearn.model_selection import 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

df = qd.get('WIKI/GOOGL')
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume',]]
df['Hl_PCT']= (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change']= (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close','Hl_PCT','PCT_change','Adj. Volume']]

# print(df.head())

forecast_col = 'Adj. Close'

df.fillna(-99999,inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

## p.4 (1st video)
# df.dropna(inplace=True)
# X= np.array(df.drop(['label'],1))
# y= np.array(df['label'])
# X = preprocessing.scale(X)
# y = np.array(df['label'])

## p.5 (2nd video)
X= np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
X= X[:-forecast_out]
X_lately = X[-forecast_out:]

df.dropna(inplace=True)
y= np.array(df['label'])
y = np.array(df['label'])


X_train, X_test, y_train,y_test = train_test_split(X,y,test_size= 0.2)

# clf = LinearRegression(n_jobs =-1)
# # clf = svm.SVR(kernel='poly')
# clf.fit(X_train,y_train)
# accuracy = clf.score(X_test,y_test)
# # print(accuracy)
# forecast_set = clf.predict(X_lately)
# print(forecast_set, accuracy,forecast_out)
# df['forecast'] = np.nan
# #print(df['Adj. Close'].head())
# last_date = df.iloc[-1].name
# last_unix = last_date.timestamp()
# one_day = 86400
# next_unix = last_unix + one_day

# for i in forecast_set:
# 	next_date = datetime.datetime.fromtimestamp(next_unix)
# 	next_unix +=one_day
# 	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]
# # print(df.head())
# # print(df.tail())

# df['Adj. Close'].plot()
# df['forecast'].plot()
# plt.legend(loc=4)
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.show()

## IN order to avoid retrain the model
# clf = LinearRegression(n_jobs =-1)
# clf.fit(X_train,y_train)
# with open('linearregression.pickle','wb') as f:
# 	pickle.dump(clf,f)

pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)

accuracy = clf.score(X_test,y_test)
# print(accuracy)
forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy,forecast_out)
df['forecast'] = np.nan
#print(df['Adj. Close'].head())
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix +=one_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]
# print(df.head())
# print(df.tail())

df['Adj. Close'].plot()
df['forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()