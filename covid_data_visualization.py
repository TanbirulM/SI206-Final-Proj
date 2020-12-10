import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime
from dateutil.parser import parse
from datetime import datetime
from matplotlib import cbook, dates
from matplotlib.ticker import Formatter
from numpy import mean

#get a list of dates from the Cases table 
def covid_date_list(db_name, table_name):
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
 
#get a list of the positive cases from teh cases table
def covid_cases_list(db_name, table_name):
   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+ db_name)
   cur = conn.cursor()
 
   covid_cases_list = []
  
   cur.execute('SELECT * FROM ' + table_name)
   rows = cur.fetchall()
 
   for i in rows:
       cases = i[1]
       covid_cases_list.append(cases)
   cur.close()
   return covid_cases_list



#using matplotlib to create a line graph comparing positive covid cases in DC over time
def create_covid_line_graph(covid_dates_list,covid_cases_list):
   ax = plt.gca()
   plt.plot(covid_dates_list,covid_cases_list)
   plt.xticks(fontsize=1)
   plt.title('Covid Cases in DC Over Time')
   plt.xlabel('Date')
   plt.ylabel('# of Positive Cases')
   plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
   plt.show()

#calculate the average daily increase in positive covid cases in DC 
def get_average_increase_in_cases(covid_cases_list):
   covid_increases = [covid_cases_list[n]-covid_cases_list[n-1] for n in range(1,len(covid_cases_list))]
  
   average_case_increase = mean(covid_increases)
 
   return print("Average daily increase in COVID-19 cases in DC is:",average_case_increase)
 
 
 
 
 
def main():
   #get dates list
   dates = covid_date_list('covid_data.db',"Cases")

   #put the dates in a proper format to be input into the X-Axis on the graph
   dates = [str(d) for d in dates]
   dates = [parse(d) for d in dates]
   dates = [d.strftime('%Y-%m-%d') for d in dates]

   #get positive cases list
   cases = covid_cases_list('covid_data.db',"Cases")

   #calculate avergae daily increase in positive cases
   get_average_increase_in_cases(cases)

   #create graph
   create_covid_line_graph(dates, cases)
 
if __name__ == "__main__":
   main()
