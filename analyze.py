import argparse
import sys

import pandas as pd
import pandas.io.sql as pdsql
import pymysql as mdb

from datetime import datetime

from tt import *


def run(args_dict):
    if len(args_dict['date'])==1:
        args_dict['date'].append(args_dict['date'][0])

    db = mdb.connect(user='{}'.format(USERNAME), host='localhost',
                     password='{}'.format(PASSWORD), db='timekeeper', charset='utf8')

    df = pdsql.read_sql('select * from timesheet', db)

    df.date = df.date.apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))

    import pdb; pdb.set_trace()
    df = df[(df.date>=args_dict['date'][0]) & (df.date>=args_dict['date'][1])]
    if args_dict['analysis']=='table':
        print df.groupby('project').apply(lambda x: (x['end'] - x['start']).sum())

    import pdb; pdb.set_trace()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze timesheet data.')
    parser.add_argument('-d', '--date', required=True, nargs='+', type=str,
                        help='Enter date(s) for analysis; enter string(s) in the '
                        'form, `mm/dd/yyy`.')
    parser.add_argument('-a', '--analysis', required=True, choices=['table', 'graph',
                        'all'], help='Enter how data should be analyzed - `table`, '
                        '`graph`, or `all`.')
    args_dict = vars(parser.parse_args())

    run(args_dict)


