# This script was written to scrape all the stations from  etrain.info site
import pandas
import ssl
import json
import sqlite3

#ignore ssl certificate exams
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

#*********************************************CREATING THE DATABASE***************************************************

conn=sqlite3.connect('train.sqlite')
cur=conn.cursor()
#cur.execute("DROP TABLE IF EXISTS Stations")
cur.execute('''CREATE TABLE IF NOT EXISTS Stations(
	st_code TEXT NOT NULL PRIMARY KEY UNIQUE,
	st_name TEXT,
	st_zone TEXT,
	st_address TEXT)''')

# ******************************FETCHING RECORDS, CLEANING, CONVERTING TO JSON AND ADDING TO DATABASE*****************

for j in range(1,340):
	url="https://etrain.info/in?PAGE=LIST--STATIONS--"+str(j)		# FETCH
	tables=pandas.read_html(url)
	tablesjson=tables[11].to_json(orient="records")					# CLEAN
	info=json.loads(tablesjson)
	for i in range(2,len(info)-1):
		cur.execute('''INSERT OR IGNORE INTO Stations(st_code,st_name,st_zone,st_address) VALUES( ? , ? , ? , ? )''',
			(info[i]["0"], info[i]["1"], info[i]["2"], info[i]["3"]))
		print(info[i]["0"], "\t", info[i]["1"], "\t", info[i]["2"], "\t", info[i]["3"])
	url=""
	conn.commit()
