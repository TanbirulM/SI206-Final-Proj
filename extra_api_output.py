import sqlite3
import os
import csv
import re
import matplotlib
import matplotlib.pyplot as plt

#grabbing data from Food_Recall table in database and putting them into a list of tuples
def food_recall_lst(db_name, table_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_name)
    cur = conn.cursor()

    data_lst = []

    cur.execute('SELECT * From ' + table_name)
    rows = cur.fetchall()
    #print(rows)
    for i in rows:
        state = i[2]
        quantity = i[5]
        quantity = quantity.replace(',', '')
        #quantity = int(''.join(filter(str.isdigit, quantity)))
        quantity = re.findall('\d+', quantity)
        if len(quantity) > 0:
            quantity = quantity[0]
        else:
            quantity = None    
        classification = i[6]

        data_lst.append((state, quantity, classification))
    cur.close()
    #print(data_lst)
    return data_lst

#returning a list of a single tuple that has the counts of the classes of food recalls
def food_recall_classifications(recall_lst):
    class_1_count = 0
    class_2_count = 0 
    class_3_count = 0

    classification_lst = []

    for i in recall_lst:
        if i[2] == 'Class I':
            class_1_count += 1
        elif i[2] == 'Class II':
            class_2_count += 1
        else:
            class_3_count += 1
    
    classification_lst.append((class_1_count, class_2_count, class_3_count))
    return classification_lst

    
def write_csv(data_lst, classification_lst):
    with open('food_recall.csv', 'w') as food_recall_dump:
        f = csv.writer(food_recall_dump, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.writerow(["State", "Quantity", "Classification"])

        for i in data_lst:
            f.writerow([i[0], i[1], i[2]])
        
        f.writerow("\n")

        f.writerow(["Class 1 Count", "Class 2 Count", "Class 3 Count"])
        for i in classification_lst:
            f.writerow([i[0], i[1], i[2]])

def create_class_chart(classification_lst):
    class_1 = classification_lst[0][0]
    class_2 = classification_lst[0][1]
    class_3 = classification_lst[0][2]

    classes = ['Class I', 'Class II', 'Class III']
    counts = [class_1, class_2, class_3]

    #plt.figure(1, figsize=(14, 4), sharey=True)
    fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    axs[0].bar(classes, counts)
    axs[1].scatter(classes, counts)
    axs[2].plot(classes, counts)
    
    fig.suptitle('Categorical Plotting of Food Recall Classifications')

    plt.savefig("classifications_chart.png")
    plt.show()

def main():
    data_lst = food_recall_lst('covid_data.db', 'Food_Recall')

    # Numerical designation (I, II, or III) that is assigned by FDA to a particular product recall that indicates the relative degree of health hazard.
    classification_lst = food_recall_classifications(data_lst)
    write_csv(data_lst, classification_lst)

    create_class_chart(classification_lst)
    
    # Products that are unlikely to cause any adverse health reaction, but that violate FDA labeling or manufacturing laws.
    print('The number of total Class I recalls in the database: ', classification_lst[0][0])

    # Products that might cause a temporary health problem, or pose only a slight threat of a serious nature.
    print('The number of total Class II recalls in the database: ', classification_lst[0][1])

    # Dangerous or defective products that predictably could cause serious health problems or death. 
    print('The number of total Class III recalls in the database: ', classification_lst[0][2])

if __name__ == "__main__":
    main()