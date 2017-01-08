import ConfigParser
import os

USERNAME = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASS')


def update_args(args):
    cfg = ConfigParser.ConfigParser()
    cfg.read('config.cfg')

    for field in ['host', 'db', 'table']:
        if not args[field]:
            args[field] = cfg.get('database', field)

    return args
