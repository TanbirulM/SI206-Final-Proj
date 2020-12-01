import csv
import matplotlib.pyplot as plt
import sqlite3
import requests
import json
import os 

def create_covid_cases_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Cases (Date INTEGER, Cases INTEGER)")
    conn.commit()

def get_request_url(date):
    base_url = "https://api.covidtracking.com"
    request_url = base_url + "/v1/states/dc/{}.json" .format(date)
    return request_url

def get_covid_cases_data(cur, conn, date):
    url = get_request_url(date)
    cur.execute("SELECT * FROM Cases WHERE Date = ?", (date, ))
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
        date = data.get('date')
        cases = data.get('positive')
        cur.execute("INSERT INTO Cases (Date, Cases) VALUES (?,?)",(date,cases))
        conn.commit()


def main():
    date_test = "20201106"

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    create_covid_cases_table(cur,conn)
    data = get_covid_cases_data(cur,conn,date_test)
    print(data)
    add_data_to_database(cur,conn,data)




if __name__ == "__main__":
    main()