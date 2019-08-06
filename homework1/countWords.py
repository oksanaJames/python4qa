# encoding=utf-8
import re
import optparse
import datetime
import traceback
import codecs
import os


def countWordAppearance():
    # add cmd help command
    parser.add_option("--pathToFile", action="store", type="string", dest="pathToFile", default=None,
                      help="Name of input file to process, required parameter")
    (options, args) = parser.parse_args()

    if not options.pathToFile:  # if no command is specified
        parser.error('No --pathToFile specified')

    fileLocation = options.pathToFile  # get the command line parameter

    # check if the filename was specified or only path to the folder
    if not os.path.isfile(fileLocation):
        parser.error("Please specify a filename in the path")

    # check if the file is utf-8 file, won't process any other files
    checkIfFileIsValid(fileLocation)

    # parse a file by line
    with open(fileLocation, 'r', encoding='utf-8-sig') as inputFile:  # open a file avoiding BOM
        inputText = inputFile.read()
    textSplittedByLine = inputText.split('\n')  # creates list with items -> 1 item = 1 line

    for line in textSplittedByLine:
        if line != '':  # avoid an empty items
            separator = "[., \-!?:;()'\"\[\]{}…\‒]+"
            wordsPerLineSeparated = list(filter(None, re.split(separator, line)))  # split the line by any of characters

            wordCount = 1
            for word in wordsPerLineSeparated:
                word = word.lower() # convert to lower case

                # store the word in dict with it's default count 1; increment count on each word repeat and update dict
                if word in wordCountsStorage:
                    wordCountExtracted = wordCountsStorage[word]
                    newWordCount = wordCountExtracted + wordCount
                    wordCountsStorage.update({word: newWordCount})
                else:
                    wordCountsStorage.update({word: wordCount})

    for item in sorted(wordCountsStorage.items()):
        word, value = item
        print("'{}' present {} time(s)".format(word,value))


def checkIfFileIsValid(fileLocation):
    try:
        f = codecs.open(fileLocation, encoding='utf-8', errors='strict')
        for line in f:
            pass
        f.close()
    except UnicodeDecodeError:
        parser.error("invalid utf-8 file")


if __name__ == '__main__':
    parser = optparse.OptionParser()
    listWithWords = []
    wordCountsStorage = {}
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()
        countWordAppearance()
    except Exception as e:
        print("\nError")
        print(e)
        traceback.print_exc()
    finally:
        duration = str(datetime.datetime.now() - start)  # print the time taken for script execution
        print('\n')
        print('command run complete in duration: %s' % duration)
        print('-----end-----')
