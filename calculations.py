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

def crime_per_category(cur,conn):
    # retrieves all data from Crime table
    cur.execute('SELECT * FROM Crimes')
    rows = cur.fetchall()

    offense_lst = []

    for i in rows:
        date = i[0]
        offense = i[1]
        offense_lst.append((date, offense))
    conn.close()
    
    #list of the amount of instances per crime category
    category_dict = {}

    category_dict["theft_other"] = 0
    category_dict["theft_auto"] = 0
    category_dict["motor_vehicle_theft"] = 0
    category_dict["robbery"] = 0
    category_dict["assault"] = 0
    category_dict["burglary"] = 0
    category_dict["homicide"] = 0
    category_dict["sex_abuse"] = 0
    category_dict["arson"] = 0

    for i in offense_lst:
        if i[1] == "THEFT/OTHER":
            category_dict["theft_other"] += 1
        elif i[1] == "THEFT F/AUTO":
            category_dict["theft_auto"] += 1
        elif i[1] == "MOTOR VEHICLE THEFT":
            category_dict["motor_vehicle_theft"] += 1
        elif i[1] == "ROBBERY":
            category_dict["robbery"] += 1
        elif i[1] == "ASSAULT W/DANGEROUS WEAPON":
            category_dict["assault"] += 1
        elif i[1] == "BURGLARY":
            category_dict["burglary"] += 1
        elif i[1] == "HOMICIDE":
            category_dict["homicide"] += 1
        elif i[1] == "SEX ABUSE":
            category_dict["sex_abuse"] += 1
        else:
            category_dict["arson"] += 1
        
    return category_dict

def write_crimecat_calc(category_dict):
    f = open('calculations.txt', 'a+')
    f.write("\n\nNumber of Crimes By Type of Offense:\n\n")
    for offense in category_dict:
        f.write(offense + ": " + str(category_dict[offense] + "\n\n"))  
    f.close()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    write_weather_calc(calc_weathercrimecorr(cur,conn))
    write_crimecat_calc(crime_per_category(cur,conn))
if __name__ == "__main__":
    main()
