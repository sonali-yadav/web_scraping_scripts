import pandas
import ssl
import json
import sqlite3


#ignore ssl certificate exams
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

# ALGORITHM:
# CREATE DATABASE TABLE FOR SCHEDULES
# FETCH TRAINS FROM DATABASE IN LOOP
# VISIT THAT URL AND GET THE SCHEDULE IN TABLE
# CONVERT TO JSON
# SAVE THE JSON DATA TO DATABASE
# CREATE A JOIN QUERY SO AS TO DEMONSTRATE THAT THE RECORDS HAVE BEEN SAVED OR NOT (OPTIONAL) 


#*********************CREATE DATABASE********************************************************

conn=sqlite3.connect('train.sqlite')
cur=conn.cursor()
#cur.execute("DROP TABLE IF EXISTS Schedules")
cur.execute('''CREATE TABLE IF NOT EXISTS Schedules(
	tr_number INTEGER NOT NULL,
	st_code TEXT,
	arrival_daytime TEXT,
	dept_daytime TEXT,
	distance_km INTEGER)''')

#*******************MAIN PROCESS LOOP********************************************************

trno=input('enter train num:')
url="https://etrain.info/in?TRAIN="+str(trno)
tables=pandas.read_html(url)
print(tables[14])
inp=input("enter y or n? ")
if inp=='y':
	tablesjson=tables[14].to_json(orient="records")
	info=json.loads(tablesjson)
	#print(json.dumps(info, indent=4))
	for i in range(2,len(info)-1):
		cur.execute('INSERT INTO Schedules(tr_number,st_code,arrival_daytime,dept_daytime,distance_km) VALUES (?,?,?,?,?)', 
			(trno,info[i]["1"],info[i]["3"],info[i]["4"],info[i]["5"]))
		print(trno,info[i]["1"],info[i]["3"],info[i]["4"],info[i]["5"])
	conn.commit()
else: print("ok!")
