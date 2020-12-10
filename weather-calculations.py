import sqlite3
import json
import os


#calculate correlation between weather(degrees of temperature) and crime by dividing number of daily crimes by daily average temperature
def calc_weathercrimecorr(cur,conn):
    cur.execute("SELECT Weather.Low, Weather.High, CrimeTotals.Crimes, CrimeTotals.Date FROM Weather JOIN CrimeTotals ON Weather.Date = CrimeTotals.Date")
    tuple_list = cur.fetchall()
    conn.commit()
    calc_dict = {}
    for tup in tuple_list:
        average = (tup[0]+tup[1])/2
        corr = tup[2]/average
        calc_dict[tup[3]] = corr
  
    return calc_dict

def write_weather_calc(cw_dict):
    f = open('calculations.txt', 'a+')
    f.write("Correlation between Daily Number of Crimes and Daily Average Temp:\n\n")
    for date in cw_dict:
        formatted_date= str(date)
        formatted_date= formatted_date[0:4] + "-" + formatted_date[4:6] + "-" + formatted_date[6:]
        f.write("On " + formatted_date + ", the correlation between daily number of crimes and daily average temperature was " + str(cw_dict[date]) + "crimes per degree of temperature (fahrenheit).\n\n")
    f.close()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    write_weather_calc(calc_weathercrimecorr(cur,conn))

if __name__ == "__main__":
    main()
