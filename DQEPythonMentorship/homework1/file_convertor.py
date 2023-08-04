# encoding=utf-8
import csv
import json

"""Create function to convert csv file to json using DictReader(), with context manager and indent=2"""


def convert_csv_to_json(input_file, output_file):
    output_structure = []
    with open(input_file, 'r') as text_file:
        structured_file = csv.DictReader(text_file)
        for row in structured_file:
            output_structure.append(row)

    with open(output_file, 'w') as notation_file:
        json.dump(output_structure, notation_file, indent=2)


if __name__ == '__main__':
    convert_csv_to_json('cars.csv', 'cars.json')
