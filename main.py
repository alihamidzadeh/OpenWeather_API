import math
import time
from datetime import datetime
import sqlite3
import requests


def sql_connector():
    con = sqlite3.connect("Weather.db")
    cur = con.cursor()
    return con,cur

def creat_table(con, cur):
    cur.execute("CREATE TABLE IF NOT EXISTS Weather(name TEXT, datetime TEXT, temp TEXT, humidity TEXT)") #, country TEXT, requestTime TEXT)")
    con.commit()

def insert_data(con, cur, data):
    cur.execute("INSERT INTO Weather values(?,?,?,?)", tuple([v for k, v in data.items()]))
    con.commit()


def proccess_data(data):
    return {"City name": data['name'], "date time": time.ctime(int(data['dt'])), "Temp": math.floor(data['main']['temp'] - 273.16),
            "Humidity": data['main']['humidity']} #, "Country": data['sys']['country'], "Request Time" : datetime.now().strftime("%H:%M:%S")}


def get_Weather_data(city='Mashhad', appid='fcd519ef5b6ba8e1133ed0f8542e0127'):
    URL = "http://api.openweathermap.org/data/2.5/weather"
    PARAMS = {'q': city, 'appid': appid}
    req = requests.get(url=URL, params=PARAMS)
    return proccess_data(req.json())


con,cur = sql_connector()
creat_table(con,cur)

while (True):
    # ct = input("Enter the city name: ")
    data_weather = get_Weather_data()
    insert_data(con,cur,data_weather)
    print(data_weather)
    time.sleep(0.5)

