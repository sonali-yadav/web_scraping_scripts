import pandas
import ssl
import json
import sqlite3


#ignore ssl certificate exams
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

#url format: https://etrain.info/in#!PAGE=runningHistory--12113--1y

trno=input('enter train num:')
url="https://etrain.info/in?PAGE=runningHistory--"+str(trno)+"--1y"
tables=pandas.read_html(url)
print(tables[17])

'''inp=input("enter y or n? ")
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
'''