import sqlite3
import os
import traceback
import datetime
from sqlite3 import Error
import csv


dbName = 'sqllite.db'


def sql_connection(dbname):
    try:
        con = sqlite3.connect(dbname)
        return con
    except Error:
        print(Error)


def execute_query(con, query):
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()


def insert_into_table(tablename, values):
    return "INSERT INTO {} VALUES{}".format(tablename, values)


def sql_fetch(con, tablename, column, value):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM {} WHERE {} = "{}"'.format(tablename, column, value))
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)


def read_file(filename):
    valuesList = []
    global headers, row
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        for row in csv_reader:
            valuesList.append(tuple(row))
    return valuesList

def main():
    try:
        projectTableCreate = "CREATE TABLE project(name text PRIMARY KEY, description text, deadline date)"
        tasksTableCreate = "CREATE TABLE tasks(id int PRIMARY KEY, priority int, details text, status text, deadline date," \
                           "completed date, project text, FOREIGN KEY (project) REFERENCES project(name))"

        # check id database exists and create if not
        if not os.path.exists(dbName):
            con = sql_connection(dbName)
        else:
            os.remove(dbName)
            con = sql_connection(dbName)

        # create tables 'project' and 'tasks'
        execute_query(con, projectTableCreate)
        execute_query(con, tasksTableCreate)

        insertValues = []
        # read csv file and insert into 'project' table
        insertValues = read_file('project.csv')
        execute_query(con, insert_into_table("project", str(insertValues).strip('[]')))
        del insertValues[:]

        # read csv file and insert into 'tasks' table
        insertValues = read_file('tasks.csv')
        execute_query(con, insert_into_table("tasks", str(insertValues).strip('[]')))
        del insertValues[:]

        # select * from tasks where project = 'REFINITIV'
        sql_fetch(con, "tasks", "project", "REFINITIV")


    except Exception as e:
        print("\nError")
        print(e)
        print('\n')
        traceback.print_exc()


if __name__ == '__main__':
    main()