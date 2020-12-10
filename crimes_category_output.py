import sqlite3
import os
import csv
import re
import matplotlib
import matplotlib.pyplot as plt

def crime_lst(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_name)
    cur = conn.cursor()

    # retrieves all data from Crime table
    cur.execute('SELECT * FROM ' + table_name)
    rows = cur.fetchall()

    offense_lst = []
   
    for i in rows:
        date = i[0]
        offense = i[1]
        offense_lst.append((date, offense))
    conn.close()
    return offense_lst

def crime_per_category(offense_lst):
    #list of the amount of instances per crime category
    category_lst = []

    theft_other = 0
    theft_auto = 0
    motor_vehicle_theft = 0
    robbery = 0
    assault = 0
    burglary = 0
    homicide = 0
    sex_abuse = 0
    arson = 0

    for i in offense_lst:
        if i[1] == "THEFT/OTHER":
            theft_other += 1
        elif i[1] == "THEFT F/AUTO":
            theft_auto += 1
        elif i[1] == "MOTOR VEHICLE THEFT":
            motor_vehicle_theft += 1
        elif i[1] == "ROBBERY":
            robbery += 1
        elif i[1] == "ASSAULT W/DANGEROUS WEAPON":
            assault += 1
        elif i[1] == "BURGLARY":
            burglary += 1
        elif i[1] == "HOMICIDE":
            homicide += 1
        elif i[1] == "SEX ABUSE":
            sex_abuse += 1
        else:
            arson += 1
        
    category_lst.append((theft_other, theft_auto, motor_vehicle_theft, robbery, assault, burglary, homicide, sex_abuse, arson))
    return category_lst

    
def write_csv(category_lst):
    with open('dc_crime_offenses.csv', 'w') as weather_dump:
        write_prices = csv.writer(weather_dump, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_prices.writerow(["THEFT/OTHER", "THEFT F/AUTO", "MOTOR VEHICLE THEFT", "ROBBERY", "ASSAULT W/DANGEROUS WEAPON", "BURGLARY", "HOMICIDE", "SEX ABUSE", "Arson"])

        for i in category_lst:
            write_prices.writerow([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]])

# This creates a pie chart using the data of a given list with three elements
def create_bar_chart(category_lst):

    x = ["THEFT/OTHER", "THEFT F/AUTO", "MOTOR VEHICLE THEFT", "ROBBERY", "ASSAULT W/ WEAPON", "BURGLARY", "HOMICIDE", "SEX ABUSE", "Arson"]
    energy = [category_lst[0][0], category_lst[0][1], category_lst[0][2], category_lst[0][3], category_lst[0][4], category_lst[0][5], category_lst[0][6], category_lst[0][7], category_lst[0][8]]

    x_pos = [i for i, _ in enumerate(x)]

    fig = plt.subplots(1, figsize=(20, 8), sharey=True)

    plt.bar(x_pos, energy, color='green')
    plt.xlabel("Offense Type")
    plt.ylabel("Number of Instances")
    plt.title("Washington DC Crimes by Category")

    plt.xticks(x_pos, x)
    plt.savefig("crimes_category_chart.png")
    plt.show()

def main():
    data_lst = crime_lst('covid_data.db', 'Crimes')
    category_lst = crime_per_category(data_lst)
    write_csv(category_lst)
    create_bar_chart(category_lst)


if __name__ == "__main__":
    main()