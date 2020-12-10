import csv
import matplotlib.pyplot as plt
import sqlite3
import requests
import json
import os 


#create table that will contain data for number of positive COVID-19 cases in DC given a date
def create_covid_cases_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Cases (Date INTEGER, Cases INTEGER)")
    conn.commit()

#get the request url to access the COVID tracking API based on the date
def get_request_url(date):
    base_url = "https://api.covidtracking.com"
    request_url = base_url + "/v1/states/dc/{}.json" .format(date)
    return request_url

#gets data from the API only if data does not already exist in Cases table
def get_covid_cases_data(cur, conn, date):
    #gets request url
    url = get_request_url(date)

    #checking to see if date is already in table
    cur.execute("SELECT * FROM Cases WHERE Date = ?", (date, ))
    exists = cur.fetchone()

    #if data not already in table, try grabbing data and returning # of positive cases
    if exists == None:
        try:
            response = requests.get(url)
            json_data = json.loads(response.text)
            cases = json_data.get['positive']
            return cases
    #if exception occurs, prints exception
        except:
            print("Exception")
            return None
    #lets me know if data does already exist in table 
    else:
        print("Data already exists")
        return None
    
#adds data to database table Cases 25 items at a time for the first 100 items
def add_data_to_database(cur, conn, dates,cases):
    cur.execute("SELECT * FROM Crimes")
    entries = cur.fetchall()
    if len(entries) == 0:
        for i in range(25):
            cur.execute("INSERT INTO Cases (Date, Cases) Values (?,?)", (dates[i], cases[i],))
            conn.commit()
        elif len(entries) == 25:
            for i in range(25,50):
                cur.execute("INSERT INTO Cases (Date, Cases) Values (?,?)", (dates[i], cases[i],))
                conn.commit()
        elif len(entries) == 50:
            for i in range(50,75):
                cur.execute("INSERT INTO Cases (Date, Cases) Values (?,?)", (dates[i], cases[i],))
                        conn.commit()
        elif len(entries) == 75:
            for i in range(75,100):
                cur.execute("INSERT INTO Cases (Date, Cases) Values (?,?)", (dates[i], cases[i],))
                conn.commit()
        elif len(entries) == 100:
            for i in range(100, len(dates)):
                cur.execute("INSERT INTO Cases (Date, Cases) Values (?,?)", (dates[i], cases[i],))
                conn.commit()



def main():

#the following lists are just creating lists of dates in the appropriate format for the API
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
    for i in range(26,31):
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
    for i in range(26,32):
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
    for i in range(26,31):
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
    for i in range(26,32):
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
    for i in range(26,32):
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
    for i in range(26,31):
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
    for i in range(26,32):
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
    for i in range(26,31):
        date_string = "202011" + str(i)
        november_dates_list2.append(date_string)

    december_dates_list = []
    for i in range(1,8):
        date_string = "2020120" + str(i)
        december_dates_list.append(date_string)

#this adds all of the lists together into one final list with every date from March 7th-December 7th in the appropriate format for the COVID API
    total_dates = []
    total_dates = [march_dates_list,april_dates_list1,april_dates_list2,may_dates_list1,may_dates_list2,june_dates_list1,june_dates_list2,july_dates_list1,july_dates_list2,august_dates_list1,august_dates_list2,september_dates_list1,september_dates_list2,october_dates_list1,october_dates_list2,november_dates_list1,november_dates_list2,december_dates_list]
    flat_dates_list = []
    for sublist in total_dates:
        for item in sublist:
            flat_dates_list.append(item)

 
#getting the current working directory, connecting to the database, and creating the Cases table
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    create_covid_cases_table(cur,conn)

#getting a list of the positive cases in chronological order to be added to the table
    cases_list = []
    for date in flat_dates_list:
        url = get_request_url(date)
        data = get_covid_cases_data(cur,conn,date)
        cases_list.append(data)
        
#adding data to Cases table based on dates list and postiive cases list
    add_data_to_database(cur,conn,flat_dates_list,cases_list)

if __name__ == "__main__":
    main()
