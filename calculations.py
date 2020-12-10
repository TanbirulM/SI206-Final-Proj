import sqlite3
import json
import os
import requests
import re



def calculateCrimeCovidCorr(cur, conn):
    cur.execute("SELECT Cases.Date, Cases.Cases, CrimeTotals.Crimes FROM Cases JOIN Crimes ON Cases.Date = CrimeTotals.Date")

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+ '/' + "covid_data.db")
    cur = conn.cursor()

if __name__ == "__main__":
    main()