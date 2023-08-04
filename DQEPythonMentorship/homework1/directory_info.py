# encoding=utf-8
import argparse
import os
from prettytable import PrettyTable
# from pwd import getpwuid
# from grp import getgrgid

"""Like Unix ls -lh create module which list directory structure
# using os.listdir, os.stat, prettytable, pwd, grp

# Modules 'pwd' and 'grp' doesn't work on Windows, so alternative way was used for Owner & Group parameters population
"""


def convert_bytes(size):
    # This function convert bytes to MB.... GB... etc
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def show_folder_structure(folder_path):
    # This function lists folder structure and display it into table format
    table = PrettyTable()
    table.field_names = ['Mode', 'Owner', 'Group', 'Size', 'File name']

    if not os.path.exists(folder_path):
        print("This directory '{}' does not exist\n".format(folder_path))
    else:
        print("----------------------------------------------")
        print("'{}' folder structure is:\n".format(folder_path))
        folder_content = os.listdir(folder_path)
        for item in folder_content:
            file_stats = os.stat(os.path.join(folder_path, item))
            # owner = getpwuid(stat(item).st_uid).pw_name
            # group = getgrgid(stat(item).st_uid).gr_name
            table.add_row([file_stats.st_mode, os.getlogin(), file_stats.st_gid, convert_bytes(file_stats.st_size), item])
        print(table)


def parse_cmd_args():
    path_help = "Path to a folder"

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help=path_help)

    cmd = parser.parse_args()
    return cmd.path


if __name__ == '__main__':
    args = parse_cmd_args()
    show_folder_structure(args)
