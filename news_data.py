from newsapi import NewsApiClient
import datetime as dt
import csv
import matplotlib.pyplot as plt
import sqlite3
import requests
import json
import os 

api_key = '9da618d792cd4e7abcef750197cbc801'
newsapi = NewsApiClient(api_key=api_key)

def create_articles_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Articles (Date INTEGER, Articles_Num INTEGER)")
    conn.commit()

def get_request_url(date):
    base_url = "https://newsapi.org"
    request_url = base_url + "/v2/everything?qInTitle='Covid'&language='en'&from={}&to={}&apiKey={}".format(date, date, api_key)
    return request_url

def get_article_data(cur, conn, date):
    url = get_request_url(date)
    cur.execute("SELECT * FROM Articles WHERE Date = ?", (date, ))
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

def add_data_to_database(cur, conn, data, date):
    if data != None:
        articles = data.get('totalResults')
        cur.execute("INSERT INTO Articles (Date, Articles_Num) VALUES (?,?)",(date,articles))
        conn.commit()

def main():
    date_test = "2020-12-02"
    #if we want to see the span of a month, you can create a date_2 variable with the date 30 days later 
    #and put it in the to parameter below

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    
    create_articles_table(cur,conn)

    data = get_article_data(cur, conn, date_test)
    
    # Not sure if we need to create a News API client object
    # data = newsapi.get_everything(cur, conn, qInTitle='Covid', language='en', from=date_test, to=date_test)
    
    print(data)
    add_data_to_database(cur,conn,data, date_test)

if __name__ == "__main__":
    main()