import argparse
import sqlite3
import sys
import warnings

import pymysql as mdb

from tt import *

warnings.filterwarnings('ignore')


def create_projects(args_dict):
    if args_dict['dbengine']=='mysql':
        sql_commands = [('''
            use {db};
            create table if not exists {table} (
                id int not null auto_increment,
                project_name varchar(128),
                project_code varchar(8),
                project_bill_code varchar(10),
                primary key (id)
            );
        '''.format(db=args_dict['db'], table=args_dict['table']))]
    elif args_dict['dbengine'] == 'sqlite':
        sql_commands = [('''
            create table if not exists {table} (
                id integer primary key autoincrement,
                project_name varchar(128),
                project_code varchar(8),
                project_bill_code varchar(10)
            );
        '''.format(table=args_dict['table']))]
    else:
        sys.exit(DB_ERROR_MESSAGE)

    return sql_commands


def run(args_dict):
    args_dict = update_args(args_dict)

    if args_dict['dbengine'] == 'mysql':
        db = mdb.connect(
            host='{}'.format(args_dict['host']),
            user='{}'.format(USERNAME),
            password='{}'.format(PASSWORD),
            autocommit=True
        )
    elif args_dict['dbengine'] == 'sqlite':
        db = sqlite3.connect('{}.db'.format(args_dict['db']), isolation_level=None)
    else:
        sys.exit(DB_ERROR_MESSAGE)

    sql_commands = create_projects(args_dict)
    if args_dict['dbengine'] == 'mysql':
        sql_commands.insert(0, 'create database if not exists {};'.format(args_dict['db']))

    sql_commands.append(('''
        insert into {table} (project_name, project_code, project_bill_code)
            values ('MyFirstProject', 'proj1', '111111');
    '''.format(table=args_dict['table'])))

    for sql in sql_commands:
        db.cursor().execute(sql)
    db.cursor().close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a project table to database.')
    parser.add_argument('-d', '--db', required=False, help='Name of the database '
                        'to create.')
    parser.add_argument('-t', '--table', required=False, help='Name of the table to '
                        'create.')
    parser.add_argument('-e', '--dbengine', required=False, choices=['mysql', 'sqlite'],
                        help='Database engine; will default to config settings.')
    parser.add_argument('--host', required=False, help='Database host; will default to '
                        'config settings.')
    args_dict = vars(parser.parse_args())

    run(args_dict)
