#屯門市廣場店
#should i name this script as transform_load.py?

import requests
import json
import sqlite3
import pytz
from datetime import datetime
import pandas as pd
import schedule
import time
import ast

conn = sqlite3.connect('sushiro_dataset.db')

quary = 'SELECT id ,name, timestamp,waitingGroup,mixedQueue FROM store'

# Fetch all results from the executed query
df = pd.read_sql_query(quary, conn)

# Close the connection
conn.close()

df['mixedQueue'] = df['mixedQueue'].apply(ast.literal_eval)
df['mixedQueue_first'] = df['mixedQueue'].apply(lambda x: x[0] if len(x) > 0 else None)

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['weekday'] = df['timestamp'].dt.day_name()

df.to_csv('sushiro_dataset.csv', index=False)