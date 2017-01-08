import argparse
import sys

import pymysql as mdb

from tt import *


def run(args_dict):
    args_dict = update_args(args_dict)

    db = mdb.connect(user='{}'.format(USERNAME), host=args_dict['host'],
                     password='{}'.format(PASSWORD), db=args_dict['db'],
                     charset='utf8', autocommit=True)

    if args_dict['close_entry']:
        sql = ('''
            select @last_row := max(id) from {table};
            update {table} set end={time} where id=@last_row;
        '''.format(table=args_dict['table'], time=args_dict['time']))
        db.cursor().execute(sql)
    else:
        if args_dict['date'] and args_dict['project']:
            db.cursor().execute('insert into {0} (date, start, project) '
                                'values (%s, %s, %s);'.format(args_dict['table']),
                                (args_dict['date'], args_dict['time'],
                                 args_dict['project']))
        else:
            sys.exit('You\'re trying to start a new entry; you must include a date '
                     'and a project.')

    db.cursor().close()
    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add entry to timesheet')
    parser.add_argument('-t', '--time', required=True, type=float, help='Enter time as '
                        'decimal/time combination. So, `8.25` represents 8:15am')
    parser.add_argument('-d', '--date', required=False, type=str, help='Enter date of '
                        'entry as a string in the form, `mm/dd/yyy`')
    parser.add_argument('-p', '--project', required=False, type=str, help='Enter client '
                        'code to which work is to be billed.')
    parser.add_argument('-c', '--close_entry', action='store_true', help='Flag to '
                        'determine if entry should be `start` or `end` for the entry; '
                        'with flag, entry is closed.')
    parser.add_argument('--host', required=False, help='Database host; will default to '
                        'config settings.')
    parser.add_argument('--db', required=False, help='Database name; will default to '
                        'config settings.')
    parser.add_argument('--table', required=False, help='Table name; will default to '
                        'config settings.')
    args_dict = vars(parser.parse_args())

    run(args_dict)
