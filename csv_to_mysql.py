import pandas as pd
empdata = pd.read_csv(r'C:\Users\stani\Documents\GitHub\2022-COVID-19-County-Data-API\us-counties-2022.csv', index_col=False, delimiter = ',')

import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',  
                        password='lm@808QS')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE covid_data")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)
try:
    conn = msql.connect(host='localhost', database='covid_data', user='root', password='lm@808QS')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS covid_data;')
        print('Creating table....')
        cursor.execute("CREATE TABLE covid_data(date varchar(255),county varchar(255),state varchar(255),fips int,cases int,deaths int)")
        print("Table is created....")
        for i,row in empdata.iterrows():
            sql = "INSERT INTO covid_data.covid_data VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)