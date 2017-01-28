import ConfigParser
import os

USERNAME = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASS')

DB_ERROR_MESSAGE = ('''You\'re trying to use a DB engine '''
                    '''that\'s not currently supported. '''
                    '''Try again, specifying `mysql` or `sqlite`.''')


def update_args(args):
    cfg = ConfigParser.ConfigParser()
    cfg.read('config.cfg')

    for field, field_value in cfg.items('database'):
        if (field not in args) or (args[field] is None):
            args[field] = field_value

    return args
