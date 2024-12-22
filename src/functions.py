import json
from PyQt5.QtCore import QDate


NULLDATE = QDate(1420, 9, 6)
NULLINDEX = -69


def save_data(object):
    print("functions: save_data entered")
    raw_json = json.dumps(object, indent=4)
    print(raw_json)
    file = open("data/data.json", "w")
    file.write(raw_json)
    file.close()

def load_data():
    file = open("data/data.json", "r")
    raw_json = file.read()
    return json.loads(raw_json)

def qdate_to_string(b):
	return format(b.day()) + "/" + format(b.month()) + "/" + format(b.year())

