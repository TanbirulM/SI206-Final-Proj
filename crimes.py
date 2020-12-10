import sqlite3
import json
import os
import requests
import re

#creates Crimes table
def setUpCrimesTable(cur, conn):
        cur.execute("CREATE TABLE IF NOT EXISTS Crimes (Date INTEGER, Offense TEXT)")
        conn.commit()

#gets data for Crimes table
def getCrimesData(cur, conn):
    url = "https://opendata.arcgis.com/datasets/f516e0dd7b614b088ad781b0c4002331_2.geojson"
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data


#pulls offenses and date commited from url and adds them to Crimes table
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
                
        #for the first 100 entries, enters 25 rows at a time
        cur.execute("SELECT * FROM Crimes")
        entries = cur.fetchall()
        if len(entries) == 0:
                for i in range(25):
                        cur.execute("INSERT INTO Crimes (Date, Offense) Values (?,?)", (dates[i], offenses[i],))
                        conn.commit()
        elif len(entries) == 25:
                for i in range(25,50):
                        cur.execute("INSERT INTO Crimes (Date, Offense) Values (?,?)", (dates[i], offenses[i],))
                        conn.commit()
        elif len(entries) == 50:
                for i in range(50,75):
                        cur.execute("INSERT INTO Crimes (Date, Offense) Values (?,?)", (dates[i], offenses[i],))
                        conn.commit()
        elif len(entries) == 75:
                for i in range(75,100):
                        cur.execute("INSERT INTO Crimes (Date, Offense) Values (?,?)", (dates[i], offenses[i],))
                        conn.commit()
        elif len(entries) == 100:
                for i in range(100, len(dates)):
                        cur.execute("INSERT INTO Crimes (Date, Offense) Values (?,?)", (dates[i], offenses[i],))
                        conn.commit()



#creates CrimeTotals Table
def setUpCrimeTotalsTable(cur,conn):
        cur.execute("CREATE TABLE IF NOT EXISTS CrimeTotals (Date INTEGER, Crimes INTEGER)")
        conn.commit()

#gets dates list for date column in CrimeTotals Table
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

#calculates daily number of crimes from Crimes Table
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

#adds daily number of crimes to CrimeTotals table
def addCrimeTotals(cur,conn,data):
        
        dates_list = []
        crime_totals_list = []
        
        for item in data:
                dates_list.append(item[0])
                crime_totals_list.append(item[1])
        
        #for the first 100 entries, enters 25 rows at a time
        cur.execute("SELECT * FROM CrimeTotals")
        entries = cur.fetchall()
        if len(entries) == 0:
                for i in range(25):
                        cur.execute("INSERT INTO CrimeTotals (Date, Crimes) Values (?,?)", (dates_list[i], crime_totals_list[i],))
                        conn.commit()
        elif len(entries) == 25:
                for i in range(25,50):
                        cur.execute("INSERT INTO CrimeTotals (Date, Crimes) Values (?,?)", (dates_list[i], crime_totals_list[i],))
                        conn.commit()
        elif len(entries) == 50:
                for i in range(50,75):
                        cur.execute("INSERT INTO CrimeTotals (Date, Crimes) Values (?,?)", (dates_list[i], crime_totals_list[i],))
                        conn.commit()
        elif len(entries) == 75:
                for i in range(75,100):
                        cur.execute("INSERT INTO CrimeTotals (Date, Crimes) Values (?,?)", (dates_list[i], crime_totals_list[i],))
                        conn.commit()
        elif len(entries) == 100:
                for i in range(100,len(dates_list)):
                        cur.execute("INSERT INTO CrimeTotals (Date, Crimes) Values (?,?)", (dates_list[i], crime_totals_list[i],))
                        conn.commit()

        
      
#creates CrimesCovidCorrelation Table
def setUpCrimesCovidCorrelationTable(cur,conn):
        cur.execute("CREATE TABLE IF NOT EXISTS CrimesCovidCorrelation (Date INTEGER, Crimes_Per_Case INTEGER)")
        conn.commit()


#Calculates number of covid cases' effect on number of crimes by dividing number of daily crimes by number of daily cases
def calculateCrimeCovidCorr(cur, conn, results):
        tuple_list = results
        crimecovid_dict = {}

        for tup in tuple_list:
                #date as key in dict
                #calculated correlation as key value
                if tup[1] == 0:
                        crimecovid_dict[tup[0]] = 'N/A'
                else:
                        crimecovid_dict[tup[0]] = tup[2]/tup[1]
       
        return crimecovid_dict

#adds calculated correlations into CrimesCovidCorrelation Table
def addDataCrimeAndCovid(cur,conn,data):
        corr_dict = calculateCrimeCovidCorr(cur,conn,data)

        #for the first 100 entries, enters 25 rows at a time
        cur.execute("SELECT * FROM CrimesCovidCorrelation")
        entries = cur.fetchall()
        if len(entries) == 0:
                for i in range(25):
                        cur.execute("INSERT INTO CrimesCovidCorrelation (Date, Crimes_Per_Case) Values (?,?)",(data[i][0],corr_dict[data[i][0]],))
                        conn.commit()
        elif len(entries) == 25:
                for i in range(25,50):
                        cur.execute("INSERT INTO CrimesCovidCorrelation (Date, Crimes_Per_Case) Values (?,?)",(data[i][0],corr_dict[data[i][0]],))
                        conn.commit()
        elif len(entries) == 50:
                for i in range(50,75):
                        cur.execute("INSERT INTO CrimesCovidCorrelation (Date, Crimes_Per_Case) Values (?,?)",(data[i][0],corr_dict[data[i][0]],))
                        conn.commit()
        elif len(entries) == 75:
                for i in range(75,100):
                        cur.execute("INSERT INTO CrimesCovidCorrelation (Date, Crimes_Per_Case) Values (?,?)",(data[i][0],corr_dict[data[i][0]],))
                        conn.commit()
        elif len(entries) == 100:
                for i in range(100,len(corr_dict)):
                        cur.execute("INSERT INTO CrimesCovidCorrelation (Date, Crimes_Per_Case) Values (?,?)",(data[i][0],corr_dict[data[i][0]],))
                        conn.commit()

#writes calculations made to text file
def writecalc(corr_dict):
        f = open("calculations.txt", 'w')
        f.write("Correlation between daily crimes and daily covid cases:\n\n")

        for date in corr_dict:
                formatted_date= str(date)
                formatted_date= formatted_date[0:4] + "-" + formatted_date[4:6] + "-" + formatted_date[6:]
                f.write("On " + formatted_date + ", the correlation between number of daily crimes and number of daily covid cases was " + str(corr_dict[date]) + " crimes per covid case.\n\n")
        f.close()

def main():
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+ '/' + "covid_data.db")
        cur = conn.cursor()
        setUpCrimesTable(cur,conn)
        setUpCrimeTotalsTable(cur,conn)
        data = getCrimesData(cur,conn)
        addData(cur,conn,data)

        #calculates crime totals once Crime table is filled
        cur.execute("SELECT * FROM Crimes")
        if len(cur.fetchall()) > 100:
                dates = getCrimeDatesList("covid_data.db","Crimes")
                crime_list = getCrimeTotals(cur,conn,dates)
                addCrimeTotals(cur,conn,crime_list)
        

        #calculates crime/covid correlation once CrimeTotals table is filled
        cur.execute("SELECT * FROM CrimeTotals")
        if len(cur.fetchall()) > 100:
                 #uses join to pull data from Crimes and Cases tables and calculate the correlation
                cur.execute("SELECT Cases.Date, Cases.Cases, CrimeTotals.Crimes FROM Cases JOIN CrimeTotals ON Cases.Date = CrimeTotals.Date")
                results = cur.fetchall()
                conn.commit()
                setUpCrimesCovidCorrelationTable(cur,conn)
                addDataCrimeAndCovid(cur,conn,results)
                writecalc(calculateCrimeCovidCorr(cur, conn, results))
        

if __name__ == "__main__":
    main()