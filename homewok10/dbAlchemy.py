from sqlalchemy import create_engine, Table, Column, Integer, Date, Numeric, String, MetaData, CheckConstraint, ForeignKey
from sqlalchemy.sql import select
import os
import traceback
from sqlite3 import Error
from collections import OrderedDict
import csv
from datetime import datetime

dbName = 'sqllite.db'
format = '%Y-%m-%d'
listWithDicts = []


def create_db_engine(db):
    return create_engine('sqlite:///{}'.format(db))


if __name__ == '__main__':
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        # check id database exists and create if not
        if not os.path.exists(dbName):
            engine = create_db_engine(dbName)
        else:
            os.remove(dbName)
            engine = create_db_engine(dbName)

        con = engine.connect()
        metadata = MetaData()

        project = Table('project', metadata, Column('name', String(50), primary_key=True),
           Column('description', String(50)),
           Column('deadline', Date)
        )

        tasks = Table('tasks', metadata, Column('id', Integer, primary_key=True),
                      Column('priority', Integer),
                      Column('details', String(50)),
                      Column('status', String(50)),
                      Column('deadline', Date),
                      Column('completed', Date, nullable=True),
                      Column('project', String(50), ForeignKey('project.name'))
        )

        metadata.create_all(engine)
        print("Created tables:\n{}".format(engine.table_names()))

        with open('project.csv', 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)

            # convert string date to python datetime objects and replace in dict
            for row in csv_reader:
                new = dict(zip(headers, row))
                for key, value in new.items():
                    if 'deadline' in key:
                        new[key] = datetime.strptime(value, format)
                listWithDicts.append(new.copy())

        # insert values to table 'project'
        con.execute(project.insert(), listWithDicts)
        del listWithDicts[:]

        with open('tasks.csv', 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)

            # convert string date to python datetime objects  and replace in dict
            for row in csv_reader:
                new = dict(zip(headers, row))
                for key, value in new.items():
                    if 'deadline' in key or 'completed' in key:
                        new[key] = datetime.strptime(value, format)
                listWithDicts.append(new.copy())

        # insert values to table 'tasks'
        con.execute(tasks.insert(), listWithDicts)
        del listWithDicts[:]

        # select * from tasks where project = 'REFINITIV'
        print("\nSelecting all records from 'tasks' table where project is 'REFINITIV'..\n")
        s = select([tasks]).where(tasks.c.project == 'REFINITIV')
        result = con.execute(s)
        for row in result:
            print(row)


    except Exception as e:
        print("\nError")
        print(e)
        print('\n')
        traceback.print_exc()
    finally:
        print('\n')
        print('-----end-----')


