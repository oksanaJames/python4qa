# encoding=utf-8
import re
import optparse
import datetime
import traceback
from collections import OrderedDict
import csv
import re
import itertools


def lower_first(iterator):
    return itertools.chain([re.sub(r"\s+", '_',next(iterator)).lower()], iterator) # we'll use this function to set csv headers to lower and replace whitespaces with '_'


def column_return():
    parser.add_option("--path_csv", action="store", type="string", dest="path_csv", default=None,
                      help="Name of csv file to process, required parameter")
    parser.add_option("--col_name", action="store", type="string", dest="col_name", default=None,
                      help="Column name of csv file to return, required parameter")


    (options, args) = parser.parse_args()

    if not options.path_csv and not options.col_name:  # if no command is specified
        parser.error('Missing parameters: --path_csv, --col_name')
    elif not options.path_csv or not options.col_name:
        parser.error('One of parameters is missing: --path_csv, --col_name')

    fileLocation = options.path_csv
    columnToReturn = options.col_name
    column_fix_spaces = re.sub(r"\s+", '_', columnToReturn).lower()

    # 1 variant
    listWithDicts = []
    with open(fileLocation, 'r') as csv_file:
        csv_read = csv.reader(csv_file)
        headers = next(csv_read)
        headers_updated = []
        for item in headers:
            newstring = re.match(r"(\w+\s\w+)", item)
            if newstring:
                replaced = re.sub(r"\s", "_", item)
                headers_updated.append(replaced)
            else:
                headers_updated.append(item)

        for row in csv_read:
            new = OrderedDict(zip(headers_updated, row))
            listWithDicts.append(new.copy())

    for item in listWithDicts:
        print(item[columnToReturn])

    # 2 variant
    # with open(fileLocation, 'r') as csv_file:
    #     csv_reader = csv.DictReader(lower_first(csv_file), delimiter=',')
    #     # print(csv_reader.fieldnames)
    #     for lines in csv_reader:
    #         print(lines[column_fix_spaces])



if __name__ == '__main__':
    parser = optparse.OptionParser()
    listWithWords = []
    wordCountsStorage = {}
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()
        column_return()
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