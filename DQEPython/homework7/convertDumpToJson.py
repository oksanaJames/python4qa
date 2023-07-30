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

def remove_from_list(inputList):
    inputList = [re.search(r"\((.*?)\)", it).group(1).replace("`", "").replace("'", "").replace(" ", "") for it in inputList if it.startswith("INSERT INTO") or it.startswith("(")]
    return inputList


def csv_convert():
    parser.add_option("--sql_dump", action="store", type="string", dest="sql_dump", default=None,
                      help="Name of csv file to process, required parameter")
    parser.add_option("--json", action="store", type="string", dest="json", default=None,
                      help="Name of json file to create, required parameter")


    (options, args) = parser.parse_args()

    if not options.sql_dump and not options.json:  # if no command is specified
        parser.error('Missing parameters: --sql_dump, --json')
    elif not options.sql_dump or not options.json:
        parser.error('One of parameters is missing: --sql_dump, --json')

    dumpLocation = options.sql_dump
    jsonLocation = options.json


    print("Extracting from dump...")
    with open(dumpLocation, 'r') as file:
        inputFile = file.readlines()
        convertedToCsv = csv.DictReader(remove_from_list(inputFile))

    print("Creating json file...")
    with open(jsonLocation, 'w') as json_file:
        json_file.write(json.dumps([remove_password(row, "password") for row in convertedToCsv], indent=4))



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