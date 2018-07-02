import pandas
import ssl
import json

#ignore ssl certificate exams
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE


url="https://etrain.info/in?TRAIN=12111"
tables=pandas.read_html(url)
print(tables[16])
tablesjson=tables[16].to_json(orient="records")
info=json.loads(tablesjson)
#print(json.dumps(info, indent=4))
