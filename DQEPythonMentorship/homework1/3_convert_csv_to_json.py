# encoding=utf-8
import csv
import json

# Create function to convert csv file to json using DictReader(), with context manager and indent=2


def csv_to_json(csvFile, jsonFile):
    jsonList = []
    with open(csvFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            jsonList.append(row)

    with open(jsonFile, 'w') as json_file:
        json.dump(jsonList, json_file, indent=2)


if __name__ == '__main__':
    csv_to_json('cars.csv', 'cars.json')
