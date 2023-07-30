# encoding=utf-8
import optparse
import datetime
import traceback
import os


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def check_folder():
    parser.add_option("--folder_path", action="store", type="string", dest="folder_path", default=None,
                      help="Folder to check, required parameter")
    parser.add_option("--filename", action="store", type="string", dest="filename", default=None,
                      help="Filename to check, required parameter")


    (options, args) = parser.parse_args()

    if not options.folder_path and not options.filename:  # if no command is specified
        parser.error('Missing parameters: --folder_path, --filename')
    elif not options.folder_path or not options.filename:
        parser.error('One of parameters is missing: --folder_path, --filename')

    folderPath = options.folder_path
    filename = options.filename
    filenamePath = os.path.join(folderPath, filename)

    print("-----------------------------------------")
    if not os.path.exists(folderPath):
        print("This directory '{}' does not exist\n".format(folderPath))
        print("Creating a directory...\n")
        os.makedirs(folderPath)
        print("Creating a file...\n")
        open(filenamePath, 'w').close()
    else:
        print("This directory '{}' exists\n".format(folderPath))
        print("\tChecking if the file inside the directory exists...\n")
        if not os.path.isfile(filenamePath):
            print("File '{}' inside the directory '{}' doesn't exist\n".format(filename, folderPath))
            print("Creating a file...\n")
            open(filenamePath, 'w').close()
        else:
            print("File '{}' inside the directory '{}' exists\n".format(filename, folderPath))

    print("-----------------------------------------")
    print("\nPrinting directory '{}' listing..\n".format(folderPath))
    folderContent = os.listdir(folderPath)
    for item in folderContent:
        print(item)

    print("\n")
    print("\tChecking file(s) metadata...\n")
    for item in folderContent:
        itemPath = os.path.join(folderPath, item)
        filesize = os.stat(itemPath).st_size
        modDate = os.stat(itemPath).st_mtime
        if os.path.isdir(itemPath):
            print("Folder '{}' with filesize: '{}', modification date: '{}'\n".format(item, convert_bytes(filesize), datetime.datetime.fromtimestamp(modDate)))
        else:
            print("File '{}' with filesize: '{}', modification date: '{}'\n".format(item, convert_bytes(filesize), datetime.datetime.fromtimestamp(modDate)))

if __name__ == '__main__':
    parser = optparse.OptionParser()
    listWithWords = []
    wordCountsStorage = {}
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()
        check_folder()
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