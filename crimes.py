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

def setUpCrimeNumberTable(cur,conn):
        cur.execute("CREATE TABLE IF NOT EXISTS CrimeTotals (Date INTEGER, Crimes INTEGER)")
        conn.commit()

def getCrimeDatesList(db_name, table_name):
   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+ db_name)
   cur = conn.cursor()

   covid_dates_list = []
     
   cur.execute('SELECT * FROM ' + table_name)
   rows = cur.fetchall()
 
   for i in rows:
       date = i[0]
       covid_dates_list.append(date)
   cur.close()
   return covid_dates_list

def getCrimeTotals(cur,conn,covid_dates_list):
        crime_totals_dict = {}
        for date in covid_dates_list:
                cur.execute("SELECT Offense FROM Crimes WHERE Date = ?", (date,))
                crimes = cur.fetchall()
                count = len(crimes)
                crime_totals_dict[date] = count
        dictionary_items = crime_totals_dict.items()
        sorted_crime_tuples = sorted(dictionary_items)
        return sorted_crime_tuples

def addCrimeTotals(cur,conn,data):
        dates_list = []
        crime_totals_list = []
        
        for item in data:
                dates_list.append(item[0])
                crime_totals_list.append(item[1])
        for i in range(166, len(dates_list)):
                cur.execute("INSERT INTO CrimeTotals (Date, Crimes) Values (?,?)", (dates_list[i], crime_totals_list[i],))
                conn.commit()

def setUpCrimeAndCovidTable(cur,conn):
        cur.execute("CREATE TABLE IF NOT EXISTS CrimesCovidCorrelation (Date INTEGER, Cases INTEGER, Crimes INTEGER, Crimes_Per_Case INTEGER)")
        conn.commit()

def addDataCrimeAndCovid(cur,conn,data):
        corr_dict = calculateCrimeCovidCorr(cur,conn,data)
        for i in range(len(corr_dict)):
                cur.execute("INSERT INTO CrimesCovidCorrelation (Date,Cases,Crimes, Crimes_Per_Case) Values (?,?,?,?)",(data[i][0],data[i][1],data[i][2],corr_dict[data[i][0]],))
                conn.commit()

def calculateCrimeCovidCorr(cur, conn, results):
        tuple_list = results
        crimecovid_dict = {}
        i = 0
        for tup in tuple_list:
                #date as key in dict
                #calculated correlation as key value
                if tup[1] == 0:
                        crimecovid_dict[tup[0]] = 'N/A'
                else:
                        crimecovid_dict[tup[0]] = tup[2]/tup[1]
                i += 1
        return crimecovid_dict


def main():
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+ '/' + "covid_data.db")
        cur = conn.cursor()
        setUpCrimesTable(cur,conn)
        setUpCrimeNumberTable(cur,conn)
       # data = getCrimesData(cur,conn)
       # addData(cur,conn,data)
       # dates = getCrimeDatesList("covid_data.db","Crimes")
       # crime_list = getCrimeTotals(cur,conn,dates)
       # addCrimeTotals(cur,conn,crime_list)

        cur.execute("SELECT Cases.Date, Cases.Cases, CrimeTotals.Crimes FROM Cases JOIN CrimeTotals ON Cases.Date = CrimeTotals.Date")
        results = cur.fetchall()
        conn.commit()
        setUpCrimeAndCovidTable(cur,conn)
        addDataCrimeAndCovid(cur,conn,results)
        
        

if __name__ == "__main__":
    main()