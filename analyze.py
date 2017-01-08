import argparse
import sys

import pandas as pd
import pandas.io.sql as pdsql
import pymysql as mdb

from datetime import datetime

from tt import *


def run(args_dict):
    args_dict = update_args(args_dict)

    if len(args_dict['date'])==1:
        args_dict['date'].append(args_dict['date'][0])
    args_dict['date'] = [datetime.strptime(x, '%m/%d/%Y') for x in args_dict['date']]

    db = mdb.connect(user='{}'.format(USERNAME), host=args_dict['host'],
                     password='{}'.format(PASSWORD), db=args_dict['db'], charset='utf8')

    df = pdsql.read_sql('select * from {table}'.format(table=args_dict['table']), db)

    df.date = df.date.apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))

    df = df[(df.date>=args_dict['date'][0]) & (df.date>=args_dict['date'][1])]
    if args_dict['analysis']=='table':
        print df.groupby(['date', 'project']).apply(lambda x: (x['end'] - x['start']).sum())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze timesheet data.')
    parser.add_argument('-d', '--date', required=True, nargs='+', type=str,
                        help='Enter date(s) for analysis; enter string(s) in the '
                        'form, `mm/dd/yyy`.')
    parser.add_argument('-a', '--analysis', required=True, choices=['table', 'graph',
                        'all'], help='Enter how data should be analyzed - `table`, '
                        '`graph`, or `all`.')
    parser.add_argument('--host', required=False, help='Database host; will default to '
                        'config settings.')
    parser.add_argument('--db', required=False, help='Database name; will default to '
                        'config settings.')
    parser.add_argument('--table', required=False, help='Table name; will default to '
                        'config settings.')
    args_dict = vars(parser.parse_args())

    run(args_dict)


