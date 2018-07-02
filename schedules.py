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

# getting all trains in a list of tuples of format [(12111,),]
cur.execute('''SELECT tr_number FROM Trains''')
trains=list(cur.fetchall())
trains=trains[6821:] # due to inconsistencies in the site's design, train 4775 crashed, hence separate script schedule_meta.py 
					# was used to extract that data. For every inconsistency, we use that script to extract data manually. Hence
					# the list is sliced from 154 because 154 is the index of train 4775. Further slices may also be done to 
					# avoid re running the loop on data that is already stored once.
					# another slice at 251, 325, 1541,1550, 2786, 2800
#print(trains)
for train in trains:
	if len(str(train[0]))==4:
		tr='0'+str(train[0])
		url="https://etrain.info/in?TRAIN="+tr
	else:
		url="https://etrain.info/in?TRAIN="+str(train[0])
	tables=pandas.read_html(url)
	#print(tables[16])
	tablesjson=tables[16].to_json(orient="records")
	info=json.loads(tablesjson)
	#print(json.dumps(info, indent=4))
	for i in range(2,len(info)-1):
		cur.execute('INSERT INTO Schedules(tr_number,st_code,arrival_daytime,dept_daytime,distance_km) VALUES (?,?,?,?,?)', 
			(train[0],info[i]["1"],info[i]["3"],info[i]["4"],info[i]["5"]))
		print(train[0],info[i]["1"],info[i]["3"],info[i]["4"],info[i]["5"])
	conn.commit()
