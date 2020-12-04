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
    request_url = base_url + "/api/location/{}/{}/" .format(woeid, date)
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
        #getting temperature in celcius form
        low = data[0].get('min_temp')
        high = data[0].get('max_temp')

        #converting temperature into fahrenheit
        low = low * (9/5) + 32
        high = high * (9/5) + 32

        cur.execute("INSERT INTO Weather (Date, Low, High) VALUES (?,?,?)",(date, low, high))
        conn.commit()


def main():
    #A WOEID (Where On Earth IDentifier) is a unique 32-bit reference identifier that identifies any feature on Earth.
    #The following is the WOEID for Washington D.C. according to https://gist.github.com/lukemelia/353493 
    woeid = '2514815'

    #date_test = "2020/4/27"

    date_lst_1 = ["2020/1/01", "2020/1/02", "2020/1/03", "2020/1/04", "2020/1/05", "2020/1/06", "2020/1/07", "2020/1/08","2020/1/09", 
        "2020/1/10","2020/1/11", "2020/1/12", "2020/1/13", "2020/1/14", "2020/1/15", "2020/1/16", "2020/1/17", "2020/1/18", "2020/1/19", 
        "2020/1/20", "2020/1/21", "2020/1/22", "2020/1/23", "2020/1/24", "2020/1/25"]
  
    date_lst_2 = ["2020/1/26", "2020/1/27", "2020/1/28", "2020/1/29", "2020/1/30", "2020/1/31",  "2020/2/01", "2020/2/02", "2020/2/03", 
            "2020/2/04","2020/2/05", "2020/2/06","2020/2/07", "2020/2/08", "2020/2/09", "2020/2/10", "2020/2/11", "2020/2/12", "2020/2/13", 
            "2020/2/14", "2020/2/15", "2020/2/16", "2020/2/17", "2020/2/18", "2020/2/19"]

    date_lst_3 = ["2020/2/20", "2020/2/21", "2020/2/22", "2020/2/23", "2020/2/24", "2020/1/25", "2020/2/26", "2020/2/27", "2020/2/28", 
            "2020/2/29","2020/3/01", "2020/3/02","2020/3/03", "2020/3/04", "2020/3/05", "2020/3/06", "2020/3/07", "2020/3/08", "2020/3/09", 
            "2020/3/10", "2020/3/11", "2020/3/12", "2020/3/13", "2020/3/14", "2020/3/15"]

    date_lst_4 = ["2020/3/16", "2020/3/17", "2020/3/18", "2020/3/19", "2020/3/20", "2020/3/21", "2020/3/22", "2020/3/23", "2020/3/24", 
            "2020/3/25","2020/3/26", "2020/3/27","2020/3/28", "2020/3/29", "2020/3/30", "2020/3/31", "2020/4/01", "2020/4/02", "2020/4/03", 
            "2020/4/04", "2020/4/05", "2020/4/06", "2020/4/07", "2020/4/08", "2020/4/09"]

    date_lst_5 = ["2020/4/10", "2020/4/11", "2020/4/12", "2020/4/13", "2020/4/14", "2020/4/15", "2020/4/16", "2020/4/17", "2020/4/18", 
            "2020/4/19","2020/4/20", "2020/4/21","2020/4/22", "2020/4/23", "2020/4/24", "2020/4/25", "2020/4/26", "2020/4/27", "2020/4/28", 
            "2020/4/29", "2020/4/30", "2020/5/01", "2020/5/02", "2020/5/03", "2020/5/04"]

    date_lst_6 = ["2020/5/05", "2020/5/06", "2020/5/07", "2020/5/08", "2020/5/09", "2020/5/10", "2020/5/11", "2020/5/12", "2020/5/13", 
            "2020/5/14","2020/5/15", "2020/5/16","2020/5/17", "2020/5/18", "2020/5/19", "2020/5/20", "2020/5/21", "2020/5/22", "2020/5/23", 
            "2020/5/24", "2020/5/25", "2020/5/26", "2020/5/27", "2020/5/28", "2020/5/29"]

    date_lst_7 = ["2020/5/30", "2020/5/31", "2020/6/01", "2020/6/02", "2020/6/03", "2020/6/04", "2020/6/05", "2020/6/06", "2020/6/07", 
            "2020/6/08","2020/6/09", "2020/6/10","2020/6/11", "2020/6/12", "2020/6/13", "2020/6/14", "2020/6/15", "2020/6/16", "2020/6/17", 
            "2020/6/18", "2020/6/19", "2020/6/20", "2020/6/21", "2020/6/22", "2020/6/23"]

    date_lst_8 = ["2020/6/24", "2020/6/25", "2020/6/26", "2020/6/27", "2020/6/28", "2020/6/29", "2020/6/30", "2020/7/01", "2020/7/02", 
            "2020/7/03","2020/7/04", "2020/7/05","2020/7/06", "2020/7/07", "2020/7/08", "2020/7/09", "2020/7/10", "2020/7/11", "2020/7/12", 
            "2020/7/13", "2020/7/14", "2020/7/15", "2020/7/16", "2020/7/17", "2020/7/18"]
    
    date_lst_9 = ["2020/7/19", "2020/7/20", "2020/7/21", "2020/7/22", "2020/7/23", "2020/7/24", "2020/7/25", "2020/7/26", "2020/7/27", 
            "2020/7/28","2020/7/29", "2020/7/30","2020/7/31", "2020/8/01", "2020/8/02", "2020/8/03", "2020/8/04", "2020/8/05", "2020/8/06", 
            "2020/8/07", "2020/8/08", "2020/8/09", "2020/8/10", "2020/8/11", "2020/8/12"]

    date_lst_10 = ["2020/8/13", "2020/8/14", "2020/8/15", "2020/8/16", "2020/8/17", "2020/8/18", "2020/8/19", "2020/8/20", "2020/8/21", 
            "2020/8/22","2020/8/23", "2020/8/24","2020/8/25", "2020/8/26", "2020/8/27", "2020/8/28", "2020/8/29", "2020/8/30", "2020/8/31", 
            "2020/9/01", "2020/9/02", "2020/9/03", "2020/9/04", "2020/9/05", "2020/9/06"]

    date_lst_11 = ["2020/9/07", "2020/9/08", "2020/9/09", "2020/9/10", "2020/9/11", "2020/9/12", "2020/9/13", "2020/9/14", "2020/9/15", 
            "2020/9/16","2020/9/17", "2020/9/18","2020/9/19", "2020/9/20", "2020/9/21", "2020/9/22", "2020/9/23", "2020/9/24", "2020/9/25", 
            "2020/9/26", "2020/9/27", "2020/9/28", "2020/9/29", "2020/9/30", "2020/10/01"]
    
    date_lst_12 = ["2020/10/02", "2020/10/03", "2020/10/04", "2020/10/05", "2020/10/06", "2020/10/07", "2020/10/08", "2020/10/09", 
            "2020/10/10", "2020/10/11","2020/10/12", "2020/10/13","2020/10/14", "2020/10/15", "2020/10/16", "2020/10/17", "2020/10/18", 
            "2020/10/19", "2020/10/20", "2020/10/21", "2020/10/22", "2020/10/23", "2020/10/24", "2020/10/25", "2020/10/26"]
        
    date_lst_13 = ["2020/10/27", "2020/10/28", "2020/10/29", "2020/10/30", "2020/10/31", "2020/11/01", "2020/11/02", "2020/11/03", 
            "2020/11/04", "2020/11/05","2020/11/06", "2020/11/07","2020/11/08", "2020/11/09", "2020/11/10", "2020/11/11", "2020/11/12", 
            "2020/11/13", "2020/11/14", "2020/11/15", "2020/11/16", "2020/11/17", "2020/11/18", "2020/11/19", "2020/11/20"]

    date_lst_14 = ["2020/11/21", "2020/11/22", "2020/11/23", "2020/11/24", "2020/11/25", "2020/11/26", "2020/11/27", "2020/11/28", 
            "2020/11/29", "2020/11/30","2020/12/01", "2020/12/02","2020/12/03", "2020/12/04"]


    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    create_covid_cases_table(cur,conn)

    index = 1
    for date in date_lst_14:
        data = get_covid_cases_data(cur, conn, date, woeid)
        add_data_to_database(cur,conn,data)
        print(index)
        index += 1

    #data = get_covid_cases_data(cur,conn,date_test, woeid)
    #print(data)
    #add_data_to_database(cur,conn,data)





if __name__ == "__main__":
    main()