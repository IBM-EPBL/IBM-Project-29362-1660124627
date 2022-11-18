import csv
import json

with open('autos_preprocessed.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    dict = 'brands{'
    for row in data:
        if(dict.__contains__(row['brand'])):
            dict
        if(row['model'] != 'not-declared'):
            dict += '{'+row['brand']+':'+row['model']+','
    dict += '}'
    json_object = json.dumps(dict, indent=4)

with open("sample.json", "w") as outfile:
  outfile.write(json_object)