import json
from csv import DictReader

def csv_to_json():
	bb_export = 'pwi-bb-client-2019-06-20.csv'
	obj = {}
	for row in DictReader(open(bb_export,'r'), delimiter=','):
	    id = row["Id"]
	    obj[id] = dict(row)

	json_obj = json.dumps(obj)
	print(json_obj)

	f = open('pwi-bb-client-2019-06-20.json', "w")
	f.write(json_obj)
	f.close()

csv_to_json()
