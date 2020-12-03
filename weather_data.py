import csv
import matplotlib.pyplot as plt
import sqlite3
import requests
import json
import os 

def create_covid_cases_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (Date INTEGER, Low INTEGER, High Integer)")
    conn.commit()

def get_request_url(date, woeid):
    base_url = "https://www.metaweather.com"
    request_url = base_url + "/api/location/{}/{}/" .format(date, woeid)
    return request_url

def get_covid_cases_data(cur, conn, date, woeid):
    url = get_request_url(date, woeid)
    cur.execute("SELECT * FROM Weather WHERE Date = ?", (date, ))
    exists = cur.fetchone()
    if exists == None:
        try:
            response = requests.get(url)
            json_data = json.loads(response.text)
            return json_data
        except:
            print("Exception")
            return None
    else:
        print("Data already exists")
        return None
    

def add_data_to_database(cur, conn, data):
    if data != None:
        date = data[0].get('applicable_date')
        low = data[0].get('min_temp')
        high = data[0].get('max_temp')
        cur.execute("INSERT INTO Weather (Date, Low, High) VALUES (?,?,?)",(date, low, high))
        conn.commit()


def main():
    date_test = "2020/4/27"
    woeid = '2514815'

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    create_covid_cases_table(cur,conn)
    data = get_covid_cases_data(cur,conn,date_test, woeid)
    print(data)
    add_data_to_database(cur,conn,data)




if __name__ == "__main__":
    main()