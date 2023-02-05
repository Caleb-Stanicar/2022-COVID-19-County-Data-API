from flask import *
import math
import json, time
import pandas as pd
import pyodbc

app = Flask(__name__)


data = pd.read_csv (r'C:\Users\stani\Documents\GitHub\2022-COVID-19-County-Data-API\us-counties-2022.csv')   
df = pd.DataFrame(data)

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=mysqlserver808;'
                      'Database=mySampleDatabase;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('''
		CREATE TABLE covid (
			date DATE,
			county nvarchar(50),
			state nvarchar(50),
            fips int,
            cases int,
            deaths int
			)
               ''')
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO covid (date, county, state, fips, cases, deaths)
                VALUES (?,?,?,?,?,?)
                ''',
                row.date, 
                row.county,
                row.state,
                row.fips, 
                row.cases,
                row.deaths
                )
conn.commit()

#test route

@app.route('/', methods=['GET'])
def home_page():

    data_set = {'Page': 'Home', 'Message': 'API is functioning', 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)

    return json_dump

#data route

@app.route('/data/', methods=['GET'])
def data_page():

    #getting data from user via /data/?county=INSERT-COUNTY-NAME&date=DATE-MM-DD

    county = str(request.args.get('county', None))
    date = str(request.args.get('date', None)) 

    #creating response

    #might need single quotes around equals
    query = f'SELECT deaths FROM covid WHERE date={date}-2022 AND county ={county}'
    deaths = pd.read_sql_query( query , conn)
    response = ''

    #if statement for data:
    if True:
        response = f'{county} experienced {deaths} deaths on {date}-2022'
    else:
        response = "NOT A VALID DATE OR COUNTY"

    #returning via json

    data_set = {'Page': 'Data', 'Message': response, 'Deaths': deaths, 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)

    return json_dump

#main

if __name__ == '__main__':
    app.run(port=8000)