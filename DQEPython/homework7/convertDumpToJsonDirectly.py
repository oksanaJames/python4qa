# encoding=utf-8
import re
import optparse
import datetime
import traceback
import json
import csv


def remove_password(rowDict, fieldToRemove):
    rowDict.pop(fieldToRemove)
    return rowDict


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

    sqlData = []
    listWithDicts = []
    print("Extracting from dump...")
    with open(dumpLocation, 'r') as file:
        inputFile = file.readlines()

        for line in inputFile:
            if line.startswith("("):
                sqlData.append([int(i) if i.isdigit() else i for i in line[1:-3].replace("'", "").split(", ")])
            elif line.startswith("INSERT INTO"):
                header = re.search(r"\((.*?)\)", line).group(1).replace("`", "").split(", ")

    for row in sqlData:
        jsonLikeDict = dict(zip(header, row))
        listWithDicts.append(remove_password(jsonLikeDict, "password"))

    print("Creating json file...")
    with open(jsonLocation, 'w') as json_file:
        json_file.write(json.dumps(listWithDicts, indent=4))



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