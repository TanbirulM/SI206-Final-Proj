import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt

#pulls data from weather table and puts it into a list of tuples
def weather_lst(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_name)
    cur = conn.cursor()

    weather_data_lst = []

    # Only retrieve the Symbol and Price information from the given table
    cur.execute('SELECT Date, Low, High From ' + table_name)
    rows = cur.fetchall()
    #print(rows)
    for i in rows:
        date = i[0]
        low = i[1]
        high = i[2]
        low = float(low)
        high = float(high)
        average = (low + high) / 2
        weather_data_lst.append((date, low, high, average))
    cur.close()
    return weather_data_lst

# categorizing the weather on each day according (by) to a scale found on:
# http://www.city-data.com/forum/weather/785422-you-what-degree-numbers-considered-hot-19.html
def get_weather_ranges(lst):
    range_lst = []
    for i in lst:
        if i[3] < 35.00:
            range_lst.append((i[0], i[1], i[2], i[3], "Frigid"))
        elif i[3] >= 35.00 and i[1] <= 48.00:
            range_lst.append((i[0], i[1], i[2], i[3], "Cold"))
        elif i[3] >= 49.00 and i[1] <= 57.00:
            range_lst.append((i[0], i[1], i[2], i[3], "Cool"))
        elif i[3] >= 58.00 and i[1] <= 74.00:
            range_lst.append((i[0], i[1], i[2], i[3], "Warm"))
        elif i[3] >= 75.00 and i[1] <= 94.00:
            range_lst.append((i[0], i[1], i[2], i[3], "Hot"))
        else:
            range_lst.append((i[0], i[1], i[2], i[3], "Blazing"))
    
    return range_lst
    
def write_csv(weather_lst):
    with open('weather_ranges.csv', 'w') as weather_dump:
        write_prices = csv.writer(weather_dump, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_prices.writerow(["Date", "Low", "High", "Average", "Weather Description"])

        for i in weather_lst:
            write_prices.writerow([i[0], i[1], i[2], i[3], i[4]])

# This creates a pie chart using the data of a given list with three elements
def create_pie_chart(range_lst):
    # Inserting the number of days in each category and priniting the output
    range_count = {'Frigid' : 0, 'Cold' : 0, 'Cool' : 0, 'Warm' : 0, 'Hot' : 0, 'Blazing' : 0}
    for i in range_lst:
        if i[4] == "Frigid":
            range_count['Frigid'] += 1
        elif i[4] == "Cold":
            range_count['Cold'] += 1
        elif i[4] == "Cool":
            range_count['Cool'] += 1
        elif i[4] == "Warm":
            range_count['Warm'] += 1
        elif i[4] == "Hot":
            range_count['Hot'] += 1
        else:
            range_count['Blazing'] += 1

    print(range_count)

    #creating pie chart using the dictionary created prior
    labels = 'Frigid', 'Cold', 'Cool', 'Warm', 'Hot'
    sizes = [range_count['Frigid'], range_count['Cold'], range_count['Cool'], range_count['Warm'], range_count['Hot']]
    explode = (0, 0.1, 0, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Pie Chart of Weather Patterns from 2019-2018")

    plt.savefig("weather_pie_chart.png")
    plt.show()

#calculates the average low temperatures between January 1, 2019 to December 4 2020
def calculate_average_low(lst):
    count = 0
    total = 0
    for i in lst:
        total += i[1]
        count += 1

    return total/count    
    
#calculates the average high temperatures between January 1, 2019 to December 4 2020    
def calculate_average_high(lst):
    count = 0
    total = 0 
    for i in lst:
        total += i[2]
        count += 1
    
    return total/count    

def main():
    data_lst = weather_lst('covid_data.db', 'Weather')
    weather_range = get_weather_ranges(data_lst)
    write_csv(weather_range)
    create_pie_chart(weather_range)
    average_low = calculate_average_low(data_lst)
    average_high = calculate_average_high(data_lst)

    print('The avererage high temerpature between 2019 and 2018 is ', average_low)
    print('The avererage high temerpature between 2019 and 2018 is ', average_high)

if __name__ == "__main__":
    main()