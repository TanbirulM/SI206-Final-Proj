import sqlite3
import json
import os
import requests
import re

def setUpCrimesTable(cur, conn):
        cur.execute("CREATE TABLE IF NOT EXISTS Crimes (Date INTEGER, Offense TEXT)")
        conn.commit()

def getCrimesData(cur, conn):
    url = "https://opendata.arcgis.com/datasets/f516e0dd7b614b088ad781b0c4002331_2.geojson"
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data



def addData(cur, conn, data):
        crimes = data["features"]
        dates = []
        offenses = []
        for crime in crimes:
                date = r"(\d\d\d\d/\d\d/\d\d)"
                date = re.findall(date, crime["properties"]["REPORT_DAT"])[0]
                date = date.replace('/', '')
                dates.append(date)
                offenses.append(crime["properties"]["OFFENSE"])
                
        #change range value to insert 25 values at a time i.e. range(25, 50); range (50, 75) etc.
        for i in range(25):
                cur.execute("INSERT INTO Crimes (Date, Offense) Values (?,?)", (dates[i], offenses[i],))
        conn.commit()

def main():
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+ '/' + "covid_data.db")
        cur = conn.cursor()
        setUpCrimesTable(cur,conn)
        data = getCrimesData(cur,conn)
        addData(cur,conn,data)
  

if __name__ == "__main__":
    main()