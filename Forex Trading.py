from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Float
import requests
import json
import time
import os
from sqlalchemy.sql import func
import sqlalchemy as db
import math
import matplotlib.pyplot as plt


engine = create_engine('sqlite:///data.sqlite')
connection = engine.connect()

meta = MetaData()
#create data table
data1 = Table(
   'AUDUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data2 = Table(
   'JPYUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data3 = Table(
   'CHFUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data4 = Table(
   'EURUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data5 = Table(
   'GBPUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data6 = Table(
   'INRUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data7 = Table(
   'RUBUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data8 = Table(
   'CNYUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data9 = Table(
   'TWDUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)

data10 = Table(
   'KRWUSD', meta, 
   Column('time', Integer), 
   Column('fx', Float), 
   Column('toet', String, primary_key = True), 
)






meta.create_all(engine)


    
query1 = db.select([db.func.round(db.func.avg(data1.c.fx), 2)])
avg_result1 = engine.execute(query1).fetchall()

query2 = db.select([db.func.round(db.func.avg(data2.c.fx), 2)])
avg_result2 = engine.execute(query2).fetchall()

query3 = db.select([db.func.round(db.func.avg(data3.c.fx), 2)])
avg_result3 = engine.execute(query3).fetchall()


query4 = db.select([db.func.round(db.func.avg(data4.c.fx), 2)])
avg_result4 = engine.execute(query4).fetchall()

query5 = db.select([db.func.round(db.func.avg(data5.c.fx), 2)])
avg_result5 = engine.execute(query5).fetchall()

query6 = db.select([db.func.round(db.func.avg(data6.c.fx), 2)])
avg_result6 = engine.execute(query6).fetchall()

query7 = db.select([db.func.round(db.func.avg(data7.c.fx), 2)])
avg_result7 = engine.execute(query7).fetchall()

query8 = db.select([db.func.round(db.func.avg(data8.c.fx), 2)])
avg_result8 = engine.execute(query8).fetchall()

query9 = db.select([db.func.round(db.func.avg(data9.c.fx), 2)])
avg_result9 = engine.execute(query9).fetchall()

query10 = db.select([db.func.round(db.func.avg(data10.c.fx), 2)])
avg_result10 = engine.execute(query10).fetchall()




#convert price into return

def price_to_return(data):
    for i in range(1, len(data)):
        ret = (data[i]-data[i-1])/data[i]
        ret_list.append(ret)
    return ret_list

#return average price for last 6 minutes
def moving_avg(data):
    average_price_all=[]
    for i in range(0,len(data)-360):
        average_price= sum(data[i:i+359])/360
        average_price_all.append(average_price)   
    return average_price_all


#Compute the STANDARD DEVIATION 
def std(data):
    mean_data=sum(data)/len(data)
    a=[]
    for i in data:
        a.append( (i-mean_data)**2)
    b = math.sqrt(sum(a)/len(a))
    return b

#Calculate the STANDARD DEVIATION every 6 minutes
def moving_std(data):
    std_price_all=[]
    for i in range(0,len(data)-360):
        std_price= std(data[i:i+359])
        std_price_all.append(std_price)
    return std_price_all

#Calculate the minimum and the maximum STANDARD DEVIATION
def find_max_min(data):
    max = data[0]
    min = data[0]
    for i in range(len(data)):
        if data[i] > max:
            max = data[i]
        if data[i] < min:
            min = data[i]
    print("maximum standard deviation:", max ,"  ;minimum standard deviation", min )

#final question 1~4
def currency(query):
    #get data
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    
    data = [i[0] for i in ResultSet]
    
    #return list
    ret_list = []
    ret_list = price_to_return(data)
    
    
    #get average std & return
    avg_std = std(data)
    avg_return = sum(ret_list)/len(ret_list)
    
    #get moving avg and std(every6mins)
    mv_avg = moving_avg(data)
    mv_std = moving_std(data)
    
    #find the largest and smallest std
    fin = find_max_min(mv_std)
    print("average standard deviation:",avg_std)
    print("average return:",avg_return)
    fin
    
    plt.plot(data)
    
    
    
#determine buy or sell
def buy_or_sell(data,cap,price_list):
    
    mv_avg = moving_avg(data)
    mv_std = moving_std(data)
    
    last5 = data[-5]
    last4 = data[-4]
    last3 = data[-3]
    last2 = data[-2]
    last1 = data[-1]
    ret_list = price_to_return(data)
    last_5_ret = ret_list[-5:-1]
    pos_count = 0
    for i in last_5_ret:
        if i > 0:
            pos_count += 1
   
    # First Strategy Bollinger Bands 
    top_edge = mv_avg[-1] + 1.75 * mv_std[-1]
    sell_out_line = mv_avg[-1] + 1.65 * mv_std[-1]
    
    bot_edge = mv_avg[-1] - 1.75 * mv_std[-1]
    buy_in_line = mv_avg[-1] - 1.65 * mv_std[-1]

    
    if last1 > sell_out_line and last1 < top_edge and cap == 1:
        print('buy at',data[-1])
        price_list.append((-data[-1]))
        cap = 0
        return cap,price_list
    
    if last1 < buy_in_line and last1 > top_edge and cap == 0:
        print('sell at',data[-1])
        price_list.append(data[-1])
        cap = 1
        return cap,price_list
    
    # Second Strategy 
    
    if last1 - last5 < 0 and pos_count >= 3 and cap == 1:
        price_list.append((-data[-1]))
        cap = 0
        print('buy at',data[-1])
        return cap,price_list

    if last1 - last5 > 0 and pos_count <= 3 and cap == 0:
        cap = 1
        print('sell at',data[-1])
        price_list.append(data[-1])
        return cap,price_list
    
    
    return cap,price_list
        
def decision(query,cap,price_list):
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()    
    data = [i[0] for i in ResultSet]

    cap,price_list = buy_or_sell(data,cap,price_list)
    return cap, price_list

def result(price_list):
    summary = sum(price_list)
    add = price_list[-1]
    if add > 0:
        summary = summary
    if add < 0:
        summary = summary + data[-1]
    
    
    print("total profit/loss:", summary)
    





timecount=0
t0=time.time()    
cap1 = 1
price_list1 = []

# download data & save the data in a database
while True:
    time.sleep(1)
    
    a1 = requests.get('https://api.polygon.io/v1/conversion/AUD/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result1 = a1.json()  
    a2 = requests.get('https://api.polygon.io/v1/conversion/JPY/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result2 = a2.json()  
    a3 = requests.get('https://api.polygon.io/v1/conversion/CHF/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result3 = a3.json()
    a4 = requests.get('https://api.polygon.io/v1/conversion/EUR/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result4 = a4.json()  
    a5 = requests.get('https://api.polygon.io/v1/conversion/GBP/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result5 = a5.json()  
    a6 = requests.get('https://api.polygon.io/v1/conversion/INR/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result6 = a6.json()
    a7 = requests.get('https://api.polygon.io/v1/conversion/RUB/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result7 = a7.json()  
    a8 = requests.get('https://api.polygon.io/v1/conversion/CNY/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result8 = a8.json()  
    a9 = requests.get('https://api.polygon.io/v1/conversion/TWD/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result9 = a9.json()
    a10 = requests.get('https://api.polygon.io/v1/conversion/KRW/USD?amount=100&precision=4&apiKey=beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq') 
    result10 = a10.json()  
    
   
    ts = time.time()

    ins1 = data1.insert().values(time = result1['last']['timestamp'], fx = result1['converted'], toet = int(ts*1000))
    ins2 = data2.insert().values(time = result2['last']['timestamp'], fx = result2['converted'], toet = int(ts*1000))
    ins3 = data3.insert().values(time = result3['last']['timestamp'], fx = result3['converted'], toet = int(ts*1000))
    ins4 = data4.insert().values(time = result4['last']['timestamp'], fx = result4['converted'], toet = int(ts*1000))
    ins5 = data5.insert().values(time = result5['last']['timestamp'], fx = result5['converted'], toet = int(ts*1000))
    ins6 = data6.insert().values(time = result6['last']['timestamp'], fx = result6['converted'], toet = int(ts*1000))
    ins7 = data7.insert().values(time = result7['last']['timestamp'], fx = result7['converted'], toet = int(ts*1000))
    ins8 = data8.insert().values(time = result8['last']['timestamp'], fx = result8['converted'], toet = int(ts*1000))
    ins9 = data9.insert().values(time = result9['last']['timestamp'], fx = result9['converted'], toet = int(ts*1000))
    ins10 = data10.insert().values(time = result10['last']['timestamp'], fx = result10['converted'], toet = int(ts*1000))

    
    
    engine.execute(ins1)
    engine.execute(ins2)
    engine.execute(ins3)
    engine.execute(ins4)
    engine.execute(ins5)
    engine.execute(ins6)
    engine.execute(ins7)
    engine.execute(ins8)
    engine.execute(ins9)
    engine.execute(ins10)
    
    


    
   

    query_1="select FX from AUDUSD"
    cap1, price_list1 = decision(query_1,cap1,price_list1)
     #query_2="select FX from AUDUSD"
     #decision(query_2,cap2,price_list2)

    if ts - t0 > 600:     
        print(result(price_list1))
        currency(query_1)
        print("AUD/USD: ", avg_result1[0])
        print("JPY/USD: ", avg_result2[0])
        print("CHF/USD: ", avg_result3[0])
        print("EUR/USD: ", avg_result4[0])
        print("GBP/USD: ", avg_result5[0])
        print("INR/USD: ", avg_result6[0])
        print("RUB/USD: ", avg_result7[0])
        print("CNY/USD: ", avg_result8[0])
        print("TWD/USD: ", avg_result9[0])
        print("KRW/USD: ", avg_result10[0])
        break
   



   