# This script was originally written to scrape all the Rajdhani Trains from  etrain.info site
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
#cur.execute("DROP TABLE IF EXISTS Trains")
cur.execute('''CREATE TABLE IF NOT EXISTS Trains(
	tr_number INTEGER NOT NULL PRIMARY KEY UNIQUE,
	tr_name TEXT,
	start_st_code TEXT,
	end_st_code TEXT)''')


# ******************************FETCHING RECORDS, CLEANING, CONVERTING TO JSON AND ADDING TO DATABASE*****************

for j in range(1,6):
	url="https://etrain.info/in?PAGE=LIST--RAJ-TRAINS--"+str(j)		# FETCH
	tables=pandas.read_html(url)
	tablesjson=tables[11].to_json(orient="records")												# CLEAN
	info=json.loads(tablesjson)
	#print(json.dumps(info, indent=4))
	for i in range(4,len(info)-1):
		cur.execute('''SELECT st_code FROM Stations WHERE st_name= ?''', (info[i]["2"],))
		start_st_code = cur.fetchone()[0]
		cur.execute('''SELECT st_code FROM Stations WHERE st_name= ?''', (info[i]["3"],))
		end_st_code = cur.fetchone()[0]

		cur.execute('''INSERT OR IGNORE INTO Trains(tr_number,tr_name,start_st_code,end_st_code) VALUES( ? , ? , ? , ? )''',
			(info[i]["0"], info[i]["1"], start_st_code, end_st_code))
		print(info[i]["0"], "\t", info[i]["1"], "\t", start_st_code, "\t", end_st_code)
	url=""
	start_st_code, end_st_code="",""
	conn.commit()
