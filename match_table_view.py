# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 19:12:35 2017


"""

import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\Maciek\Desktop\database.sqlite")
df = pd.read_sql_query("""SELECT * FROM Match
                           """, conn)
xmls = df[['goal','shoton','shotoff', 'foulcommit','card','cross','corner','possession']]
conn.close()