from bs4 import BeautifulSoup 
import requests
import sqlite3
import os

# Sets up the database and inputs the necessary data gained from the web scraping
def setUp_db(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (Symbol TEXT, Name TEXT, Price TEXT, Performance TEXT, Rating TEXT)''')

    #add new data to db file

    cur.close()

# Getting the data from the webpage
def place_holder(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")

    #data scraping

def main():
    web_scraper('website_place_holder')
    setUp_db('db_file_place_holder', 'table_place_holder')

if __name__ == "__main__":
    main()