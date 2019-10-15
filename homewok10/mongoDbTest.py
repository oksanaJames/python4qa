from pymongo import MongoClient
import traceback
from datetime import datetime, date
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select
import dbSqllite


dbName = 'sqllite.db'
datetimeFormat = '%Y-%m-%d'
projectToInsert = []
tasksToInsert = []

def create_db_engine(db):
    engine = create_engine('sqlite:///{}'.format(db))
    con = engine.connect()
    return engine, con


def convert_datetime(value, format):
    lst = list(value)
    for idx, el in enumerate(lst):
        if isinstance(el, date):
            lst[idx] = datetime.strftime(el, format)
    value = tuple(lst)
    return value


def _connect_mongo(host, port, username, password, db):
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def build_json(header, tableData):
    dataList = []
    for row in tableData:
        rowNew = convert_datetime(row, datetimeFormat)
        jsonLikeDict = dict(zip(header, rowNew))
        dataList.append(jsonLikeDict.copy())
    return dataList


if __name__ == '__main__':
    try:
        print('\n')
        print('-----start-----')
        print('\n')

        # running sqlite create tables
        print("sqlite database and tables are created...\n")
        dbSqllite.main()

        # connect to sqllite db and get tables
        engine, con = create_db_engine(dbName)

        print("\nsqllite db tables:")
        print(engine.table_names())

        metadata = MetaData()
        project = Table('project', metadata, autoload=True, autoload_with=engine)
        tasks = Table('tasks', metadata, autoload=True, autoload_with=engine)

        # get columns names from 'project'
        projectColumns = project.columns.keys()

        # get all data froom 'project'
        selectQuery = select([project])
        projectQuery = con.execute(selectQuery)
        projectData = projectQuery.fetchall()

        # build json from 'project'
        projectToInsert = build_json(projectColumns, projectData)

        # get columns names from 'tasks'
        tasksColumns = tasks.columns.keys()

        # get all data from 'tasks'
        selectQuery = select([tasks])
        tasksQuery = con.execute(selectQuery)
        tasksData = tasksQuery.fetchall()

        # build json from 'tasks'
        tasksToInsert = build_json(tasksColumns, tasksData)

        # mongodb connect
        mongo = _connect_mongo(host='localhost', port=27017, username='', password='', db='oxana')

        # create collections from sqllite tables
        projectTable = mongo["project"]
        projectInsert = projectTable.insert_many(projectToInsert)

        tasksTable = mongo["tasks"]
        tasksInsert = tasksTable.insert_many(tasksToInsert)

        # select all project names where status is 'cancelled'
        print("\n-------")
        print("mongoDB -> Project names where tasks status is 'cancelled'")
        searchQuery = {'status': 'cancelled'}
        cancelledProject = tasksTable.find(searchQuery, {"project": 1, "status": 1, "_id": 0})
        for item in cancelledProject:
            print(item)


    except Exception as e:
        print("\nError")
        print(e)
        traceback.print_exc()
    finally:
        print('\n')
        print('-----end-----')
