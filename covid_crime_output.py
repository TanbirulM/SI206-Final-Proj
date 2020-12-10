import sqlite3
import os
import csv
import re
import matplotlib
import matplotlib.pyplot as plt

def crime_covid_lst(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_name)
    cur = conn.cursor()

    # Only retrieve the Symbol and Price information from the given tablepap
    cur.execute('SELECT * From ' + table_name)
    rows = cur.fetchall()

    data_lst = []
    #print(rows)
    for i in rows:
        date = i[0]
        cases = i[1]
        crimes = i[2]
        correlation = i[3]
        if correlation == "N/A":
            correlation = None
        data_lst.append((date, cases, crimes, correlation))
    cur.close()
    return data_lst

def get_date_lst(data_lst):
    date_lst = []
    for i in data_lst:
        date_lst.append(i[0])
    
    print(len(date_lst))
    return date_lst

def get_cases_lst(data_lst):    
    cases_lst = []
    for i in data_lst:
        if i[1] == 0:
            i[1] == None
        cases_lst.append(i[1])

    print(len(cases_lst))
    return cases_lst

def get_crimes_lst(data_lst):
    crimes_lst = []
    for i in data_lst:
        crimes_lst.append(i[2])
    
    print(len(crimes_lst))
    return crimes_lst

# This creates a pie chart using the data of a given list with three elements
def create_double_line_chart(data_lst):
    #data for plotting
    y = get_date_lst(data_lst)
    d1 = get_cases_lst(data_lst)
    d2 = get_crimes_lst(data_lst)
    
    days = []
    i = 0
    while i < len(y):
        days.append(i)
        i += 1

    # create the line graph
    fig, ax = plt.subplots()
    ax.plot(days, d1, "co-", label="Covid Cases")
    ax.plot(days, d2, "mo-", label="Crimes")
    ax.legend()
    ax.set_xlabel('Days')
    ax.set_ylabel('Instances of Covid/Crimes')
    ax.set_title('Covid Cases per day vs Crimes per day')
    ax.grid()

    # save the line graph
    fig.savefig("covid_vs_crime.png")

    # show the line graph
    plt.show() 
  

def create_scatterplot_high_low(data_lst):

    date = []
    correlation = []
    index = 0
    for i in data_lst:
        date.append(index)
        correlation.append(i[3])
        index += 1

    #print(date)
    #print(correlation)
    plt.scatter(date, correlation, s=3)
    
    plt.title("Correlation of  Covid-Crime Cases in DC by Date")
    plt.ylabel("Crimes Per Day Divided by Covid Cases Per Day")
    plt.xlabel("Days (03/07/2020 - 12/7/2020)")

    plt.savefig("correlation_scatterplot.png")
    plt.show()


def main():
    data_lst = crime_covid_lst('covid_data.db', 'CrimesCovidCorrelation')
    create_double_line_chart(data_lst)
    create_scatterplot_high_low(data_lst)


if __name__ == "__main__":
    main()