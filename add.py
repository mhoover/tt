import argparse
import sys

import pymysql as mdb

from tt import *


def run(args_dict):
    db = mdb.connect(user='{}'.format(USERNAME), host='localhost',
                     password='{}'.format(PASSWORD), db='timekeeper', charset='utf8')

    if args_dict['close_entry']:
        sql = ('SELECT @last_row := MAX(id) from timesheet; UPDATE timesheet SET '
               'end=%s WHERE id=@last_row')
        db.cursor().execute(sql, args_dict['time'])
    else:
        if args_dict['date'] and args_dict['client']:
            db.cursor().execute('INSERT INTO timesheet (date, start, project) '
                                'VALUES (%s, %s, %s)', (args_dict['date'],
                                args_dict['time'], args_dict['client']))
        else:
            sys.exit('You\'re trying to start a new entry; you must include a date '
                     'and a client.')

    db.cursor().close()
    db.commit()
    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add entry to timesheet')
    parser.add_argument('--time', required=True, type=float, help='Enter time as '
                        'decimal/time combination. So, `8.25` represents 8:15am')
    parser.add_argument('--date', required=False, type=str, help='Enter date of '
                        'entry as a string in the form, `mm/dd/yyy`')
    parser.add_argument('--client', required=False, type=str, help='Enter client '
                        'code to which work is to be billed.')
    parser.add_argument('--close_entry', action='store_true', help='Flag to determine '
                        'if entry should be `start` or `end` for the entry; with flag, '
                        'entry is closed.')

    args_dict = vars(parser.parse_args())

    run(args_dict)
