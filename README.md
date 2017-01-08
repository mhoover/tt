# tt
## Introduction
`tt` (time-track) is a mysql-based program to keep track of time (for consultants, etc.) using Python commmands. It is a general -- and very simple -- time tracking program. A database has the following values:

* `date`: Should entered as 'mm/dd/yyyy' (as a string).
* `start`: The time one starts working; recorded as a decimal/time combination. So, `8.25` would represent 8:15am and `17.75` would represent 5:45pm.
* `end`: The time one ends working; recorded as a decimal/time combination (see above).
* `project`: A string (up to 8 characters long) for identify the project to charge against.

### Configuration file
There is a configuration file that is expected as a well called `config.cfg` (see `config.cfg.example`) that takes care of specificing some values that might be unlikely to change very often (host, database, table). These are set __only__ if not set at the command line with the Python scripts.

## Use
### Initializing the time-tracking database
To set up a time-tracking database, one must have mysql (currently 5.7.17) installed locally on their machine. Then, using the `create.py` script, set up the database with a database name and table. A user can add additional tables into the same named database. Each time a table is initialized, a test entry is created. Usage is as follows:

```
$ python create.py -d my-time-db -t my-time-table
```

### Adding entries
To be expanded upon soon..

### Analyzing entries
To be expanded upon soon..
