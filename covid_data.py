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

    march_dates_list = []
    for i in range (7,32):
        if i < 10:
            date_string = "2020030" + str(i)
        else: 
            date_string = "202003" + str(i)
        march_dates_list.append(date_string)

    april_dates_list1 = []
    for i in range(1,26):
        if i < 10:
            date_string = "2020040" + str(i)
        else: 
            date_string = "202004" + str(i)
        april_dates_list1.append(date_string)
    
    april_dates_list2 = []
    for i in range(27,31):
        date_string = "202004" + str(i)
        april_dates_list2.append(date_string)

    may_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020050" + str(i)
        else: 
            date_string = "202005" + str(i)
        may_dates_list1.append(date_string)
    
    may_dates_list2 = []
    for i in range(27,32):
        date_string = "202005" + str(i)
        may_dates_list2.append(date_string)

    june_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020060" + str(i)
        else: 
            date_string = "202006" + str(i)
        june_dates_list1.append(date_string)
    
    june_dates_list2 = []
    for i in range(27,31):
        date_string = "202006" + str(i)
        june_dates_list2.append(date_string)

    july_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020070" + str(i)
        else: 
            date_string = "202007" + str(i)
        july_dates_list1.append(date_string)
    
    july_dates_list2 = []
    for i in range(27,32):
        date_string = "202007" + str(i)
        july_dates_list2.append(date_string)

    august_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020080" + str(i)
        else: 
            date_string = "202008" + str(i)
        august_dates_list1.append(date_string)
    
    august_dates_list2 = []
    for i in range(27,32):
        date_string = "202008" + str(i)
        august_dates_list2.append(date_string)
    

    september_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020090" + str(i)
        else: 
            date_string = "202009" + str(i)
        september_dates_list1.append(date_string)
    
    september_dates_list2 = []
    for i in range(27,31):
        date_string = "202009" + str(i)
        september_dates_list2.append(date_string)

    october_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020100" + str(i)
        else: 
            date_string = "202010" + str(i)
        october_dates_list1.append(date_string)
    
    october_dates_list2 = []
    for i in range(27,32):
        date_string = "202010" + str(i)
        october_dates_list2.append(date_string)

    november_dates_list1 = []
    for i in range (1,26):
        if i < 10:
            date_string = "2020110" + str(i)
        else: 
            date_string = "202011" + str(i)
        november_dates_list1.append(date_string)
    
    november_dates_list2 = []
    for i in range(27,31):
        date_string = "202011" + str(i)
        november_dates_list2.append(date_string)

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    create_covid_cases_table(cur,conn)

    for date in march_dates_list:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in april_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in april_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)
    
    for date in may_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)
    
    for date in may_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in june_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in june_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in july_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in july_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in august_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in august_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in september_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in september_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in october_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in october_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in november_dates_list1:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)

    for date in november_dates_list2:
        data = get_covid_cases_data(cur,conn,date)
        add_data_to_database(cur,conn,data)




if __name__ == "__main__":
    main()
