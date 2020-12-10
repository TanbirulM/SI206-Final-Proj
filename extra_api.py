import csv
import matplotlib.pyplot as plt
import sqlite3
import requests
import json
import os 

def create_food_recall_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Food_Recall (event_id, city, state, recall_number INTEGER, product_description, product_quantity, classification, reason_for_recall)")
    conn.commit()

def get_request_url(search_query, search_limit):
    base_url = "https://api.fda.gov"
    request_url = base_url + "/food/enforcement.json?search=distribution_pattern:{}&limit={}" .format(search_query, search_limit)
    return request_url

def get_food_recall_data(cur, conn, search_query, search_limit):
    url = get_request_url(search_query, search_limit)
    cur.execute("SELECT * FROM Food_Recall")
    #exists = cur.fetchone()
    response = requests.get(url)
    #json_data = response
    json_data = json.loads(response.text)
    return json_data

# adding the selected data to the table within the database    
def add_data_to_database(cur, conn, data):
    results_data = data["results"]
    for i in results_data:
        event_id = i.get('event_id')
        city = i.get('city')
        state = i.get('state')
        recall_number = i.get('recall_number')
        product_description = i.get('product_description')
        product_quantity = i.get('product_quantity')
        classification = i.get('classification')
        reason = i.get('reason_for_recall')

        cur.execute('''INSERT INTO Food_Recall (event_id, city, state, recall_number, product_description, product_quantity, classification, reason_for_recall) 
                VALUES (?,?,?,?,?,?,?,?)''',(event_id, city, state, recall_number, product_description, product_quantity, classification, reason))
        conn.commit()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()
    create_food_recall_table(cur,conn)

    search_query = "nationwide"
    search_limit = 100

    # we are searching the records in the food enforcement report endpoint for matches with nationwide in the distribution_pattern field
    # We are requesting to see the first 100 records that match.
    data = get_food_recall_data(cur, conn, search_query, search_limit)
    add_data_to_database(cur,conn,data)





if __name__ == "__main__":
    main()