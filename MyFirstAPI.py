import pandas as pd
import snowflake.connector as sf
import os
import json
import time

from flask import Flask, request
app = Flask(__name__)

# Setup the environment variables
sf_username = os.environ['snowflake_username']
sf_password = os.environ['snowflake_password']
sf_account= os.environ['snowflake_account']

# Store the snowflake worksheet information
sf_warehouse = 'WH_DWH'
sf_role = 'SYSADMIN'
sf_schema = 'PUBLIC'
sf_database = 'DEMO_DB'


#Create a connection to snowflake
global conn
conn = sf.connect(
    user=sf_username, 
    password = sf_password,
    account = sf_account)

# Configure the snowflake warehouse 

conn.cursor().execute('use role {}'.format(sf_role))

#conn.cursor().execute('use warehouse {}'.format(sf_warehouse))
conn.cursor().execute(f"""use warehouse {sf_warehouse}""")

conn.cursor().execute('use database {}'.format(sf_database))
conn.cursor().execute('use schema {}'.format(sf_schema))


#Method to display data 
cr = conn.cursor()
#sql1 = 'select * from customers limit 10' 
#cr.execute(sql1)

# Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
#df = cr.fetch_pandas_all()
#print(df.head(1000))

def customers_data(market_segment, conn):
    global customers
    sql = f"""select * from customers where upper(c_mktsegment) = upper('{market_segment}') limit 200"""
    customers = pd.read_sql(sql, conn)
    #cr.execute(sql)
    #customers = cr.fetch_pandas_all()
    #Data Processing
    #Fetch only accounts whose account balance is greater than 5000
    customers_processed = customers[customers['C_ACCTBAL'] > 0 ]
    return{"data":json.loads(customers_processed.to_json(orient='records'))} 
    
data= customers_data('BUILDING', conn)
json_data = json.dumps(data)
print(json_data)  
