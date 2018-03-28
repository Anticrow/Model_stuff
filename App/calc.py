import requests
import json
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import Perceptron
import numpy as np

count = 0
price_list = []
date_list = []
#columns = ["date", "price"]
#price_df = pd.DataFrame(columns = columns)
##using api to import price movement every 5 minutes
#воткнуть исторические данные по ценам и другие данные в модель сюда
#print (price_df)

import time
starttime=time.time()
while True:
  response = requests.get("https://blockchain.info/ru/ticker")
  data_raw = json.loads(response.content)  
  count +=1
  print ("tick", count)
  date = (pd.to_datetime('now'))
  usd = data_raw["USD"]['last'] #working with JSON file to look through the api request
  usd = float(usd)
  print(usd)
  price_list.append(usd)
  date_list.append(date) #creating list and appending date and time
  dict_price_date = {'Date': date_list, "Price": price_list} #creating dictionary from 2 lists
  df_date_time = pd.DataFrame(dict_price_date) #converting dictionary to data frame
  
  if count >= 2:
      df_date_time['Diff'] = df_date_time.Price.diff().shift(-1)
      df_date_time.Diff = df_date_time.Diff.shift(1)
      df_date_time["Bool"] = np.where(df_date_time['Diff']>=0, 1, 0)
      
  #print(df_date_time)
  #print(df_date_time.dtypes)
  
  if count >= 3:
      df_date_time_clean = df_date_time.dropna(axis=0)
      df_date_time_clean.to_csv('data_spider.csv', sep = ',')
      #print (df_date_time_clean)
      model = MLPClassifier(solver='sgd')
      model_1 = Perceptron()
      x = df_date_time_clean[["Price"]]
      y = df_date_time_clean[["Bool"]]
      model.fit(x, y)
      model_1.fit(x,y)
      #print (model.predict(x))
      print ("MLP accuracy is:", model.score(x,y), "% while Perceptron accuracy is:", model_1.score(x,y), "% after", count, "ticks")
      
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))
