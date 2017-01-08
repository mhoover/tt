import argparse
import sys
import warnings

import pymysql as mdb

from tt import *

warnings.filterwarnings('ignore')


def run(args_dict):
    args_dict = update_args(args_dict)

    db = mdb.connect(host='{}'.format(args_dict['host']), user='{}'.format(USERNAME),
                     password='{}'.format(PASSWORD), autocommit=True)
    sql = ('''
        use {db};
        create table {table} (
            id int not null auto_increment,
            date varchar(10),
            start decimal(4, 2),
            end decimal(4, 2),
            project varchar(8),
            primary key (id)
        );
        insert into {table} (date, start, end, project) values ('01/01/2016', 0, 1, 'test');
    '''.format(db=args_dict['db'], table=args_dict['table']))
    db.cursor().execute('create database if not exists {}'.format(args_dict['db']))
    db.cursor().execute(sql)
    db.cursor().close()
    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add entry to timesheet')
    parser.add_argument('-d', '--db', required=True, help='Name of the database '
                        'to create.')
    parser.add_argument('-t', '--table', required=True, help='Name of the table to '
                        'create.')
    parser.add_argument('--host', required=False, help='Database host; will default to '
                        'config settings.')
    args_dict = vars(parser.parse_args())

    run(args_dict)