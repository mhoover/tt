import ConfigParser
import os

USERNAME = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASS')


def update_args(args):
    cfg = ConfigParser.ConfigParser()
    cfg.read('config.cfg')

    for field, field_value in cfg.items('database'):
        if (field not in args) or (args[field] is None):
            args[field] = field_value

    return args
