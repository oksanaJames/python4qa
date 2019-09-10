# encoding=utf-8
import re
import optparse
import datetime
import traceback
import json
import csv



def remove_password(rowDict, fieldToRemove):
    rowDict.pop(fieldToRemove)
    for k, v in rowDict.items():
        if rowDict[k].isdigit():
            rowDict[k] = int(v)
    return rowDict


def csv_convert():
    parser.add_option("--csv", action="store", type="string", dest="csv", default=None,
                      help="Name of csv file to process, required parameter")
    parser.add_option("--json", action="store", type="string", dest="json", default=None,
                      help="Name of json file to create, required parameter")


    (options, args) = parser.parse_args()

    if not options.csv and not options.json:  # if no command is specified
        parser.error('Missing parameters: --csv, --json')
    elif not options.csv or not options.json:
        parser.error('One of parameters is missing: --csv, --json')

    csvLocation = options.csv
    jsonLocation = options.json

    print("Extracting from csv...")
    with open(csvLocation, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        outputjson = json.dumps([remove_password(row, "password") for row in csv_reader], indent=4)

    print("Creating json file...")
    with open(jsonLocation, 'w') as json_file:
        json_file.write(outputjson)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    listWithWords = []
    wordCountsStorage = {}
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()
        csv_convert()
    except Exception as e:
        print("\nError")
        print(e)
        print('\n')
        traceback.print_exc()
    finally:
        duration = str(datetime.datetime.now() - start)  # print the time taken for script execution
        print('\n')
        print('command run complete in duration: %s' % duration)
        print('-----end-----')