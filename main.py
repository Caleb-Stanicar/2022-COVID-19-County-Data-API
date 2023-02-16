from flask import *
import math
import json, time
import pandas as pd
import mysql.connector

app = Flask(__name__)

#test route

@app.route('/', methods=['GET'])
def home_page():

    data_set = {'Page': 'Home', 'Message': 'API is functioning', 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)

    return json_dump

#data route

@app.route('/data/', methods=['GET'])
def data_page():

    #getting data from user via /data/?county=INSERT-COUNTY-NAME&date=2022-MM-DD

    county = "missoula"
    date = "2022-12-01"
    #county = str(request.args.get('county', None))
    #date = str(request.args.get('date', None)) 

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='covid_data',
                                            user='root',
                                            password='INSERT PASSWORD')

        #creating response

        #might need single quotes around equals
        sql_select_Query = f"SELECT * FROM covid_data.covid_data WHERE date = \"{date}\" and county = \"{county}\""
        response = ''

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        print("\nPrinting each row")
        print(records)
        deaths = records[0][5]

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        data_set = {'Page': 'Data', 'Message': "Error reading data from MySQL table", 'Timestamp': time.time()}
        json_dump = json.dumps(data_set)
        print(json_dump)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    #if statement for data:
    if records != None:
        response = f'{county} experienced {deaths} total deaths as of {date}'
    else:
        response = "NOT A VALID DATE OR COUNTY"

    #returning via json

    data_set = {'Page': 'Data', 'Message': response, 'Deaths': deaths, 'Fips': records[0][3], 'Cases': records[0][4], 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)

    return json_dump

#main

if __name__ == '__main__':
    app.run(port=8000)