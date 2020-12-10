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
        correlation = i[1]
        # if there is no correlation, change 'N/A' to None so calculations can be made on that date
        if correlation == "N/A":
            correlation = None
        data_lst.append((date, correlation))
    cur.close()
    return data_lst
  
# scatter plot to show the correlation of covid and crime per day
def create_scatterplot(data_lst):

    date = []
    correlation = []
    index = 0
    for i in data_lst:
        date.append(index)
        correlation.append(i[1])
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
    create_scatterplot(data_lst)


if __name__ == "__main__":
    main()