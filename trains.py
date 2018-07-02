# This script was written to scrape all the Trains from  etrain.info site
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
cur.execute('''CREATE TABLE IF NOT EXISTS Trains(
	tr_number INTEGER NOT NULL PRIMARY KEY UNIQUE,
	tr_name TEXT,
	start_st_code TEXT NULL,
	end_st_code TEXT NULL)''')

#*************************CREATING THE SET OF URLS THAT WILL BE TRAWLED AND THEIR RANGES********************************

urls=[
	"https://etrain.info/in?PAGE=LIST--RAJ-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--SHT-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--JSHT-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--GRB-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--PRM-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--SF-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--EXP-TRAINS--",
	"https://etrain.info/in?PAGE=LIST--PASS-TRAINS--",
]
ranges=[[1,6],[1,4],[1,3],[1,4],[1,3],[1,50],[1,73],[1,158]]

# ******************************FETCHING RECORDS, CLEANING, CONVERTING TO JSON AND ADDING TO DATABASE*****************
a=0
for url in urls:
	r1,r2=ranges[a][0],ranges[a][1]
	print('r1= ',r1, " and r2= ",r2)
	for j in range(r1,r2):
		serviceurl=url+str(j)
		print(serviceurl)																		# FETCH
		tables=pandas.read_html(serviceurl)
		tablesjson=tables[11].to_json(orient="records")												# CLEAN
		info=json.loads(tablesjson)
		start_st_code, end_st_code="",""
		#print(json.dumps(info, indent=4))
		for i in range(4,len(info)-1):
			if(cur.execute('''SELECT st_code FROM Stations WHERE st_name= ?''', (info[i]["2"],))):
				start_st_code = cur.fetchone()[0]
			elif(cur.execute('''SELECT st_code FROM Stations WHERE st_name= ?''', (info[i]["3"],))):
				end_st_code = cur.fetchone()[0]
			else: continue

			cur.execute('''INSERT OR IGNORE INTO Trains(tr_number,tr_name,start_st_code,end_st_code) VALUES( ? , ? , ? , ? )''',
				(info[i]["0"], info[i]["1"], start_st_code, end_st_code))
			print(info[i]["0"], "\t", info[i]["1"], "\t", start_st_code, "\t", end_st_code)
		serviceurl=""
		conn.commit()
	a=a+1
