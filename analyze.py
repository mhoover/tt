import argparse
import subprocess
import sys

import pandas as pd
import pandas.io.sql as pdsql
import pymysql as mdb

from datetime import datetime

from tt import *


def write_plot(d, nbr):
    for i in xrange(1, nbr):
        if i==1:
            gnu = 'plot "-" u 1:2 t "{}" w lp'.format(d.columns[i])
        else:
            gnu += ', "-" u 1:2 t "{}" w lp'.format(d.columns[i])
    gnu += '\n'
    return gnu


def make_graph(d):
    plot_statement = write_plot(d, d.shape[1])

    gp = subprocess.Popen(args_dict['gnuplot'], stdin=subprocess.PIPE)
    gp.stdin.write('set terminal dumb 90 30\n')
    gp.stdin.write('set xdata time\n')
    gp.stdin.write('set timefmt "%m/%d/%Y"\n')
    gp.stdin.write(plot_statement)
    for col in xrange(1, d.shape[1]):
        for row in xrange(d.shape[0]):
            gp.stdin.write('{} {}\n'.format(d.ix[row, 0], d.ix[row, col]))
        gp.stdin.write('e\n')
    gp.stdin.flush()


def run(args_dict):
    args_dict = update_args(args_dict)

    if len(args_dict['date'])==1:
        args_dict['date'].append(args_dict['date'][0])
    args_dict['date'] = [datetime.strptime(x, '%m/%d/%Y') for x in args_dict['date']]

    db = mdb.connect(user='{}'.format(USERNAME), host=args_dict['host'],
                     password='{}'.format(PASSWORD), db=args_dict['db'], charset='utf8')

    df = pdsql.read_sql('select * from {table}'.format(table=args_dict['table']), db)

    df.date = df.date.apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))

    df = df[(df.date>=args_dict['date'][0]) & (df.date<=args_dict['date'][1])]

    vals = df.groupby(['date', 'project']).apply(lambda x: (x['end'] - x['start']).sum())
    graph = (vals
             .reset_index()
             .pivot(index='date', columns='project', values=0)
             .reset_index(level=0)
             .fillna(0))
    graph.date = graph.date.apply(lambda x: datetime.strftime(x, '%m/%d/%Y'))

    if args_dict['analysis']=='table':
        print vals
    elif args_dict['analysis']=='graph':
        make_graph(graph)
    else:
        print vals
        make_graph(graph)


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
