# tt
## Introduction
`tt` (time-track) is a mostly shell-based program to keep track of time (for consultants, etc.). It is a general -- and very simple -- time tracking program. It uses a mysql database to track entries with the following values:

* `date`: Should entered as 'mm/dd/yyyy' (as a string).
* `start`: The time one starts working; recorded as a decimal/time combination. So, `8.25` would represent 8:15am and `17.75` would represent 5:45pm.
* `end`: The time one ends working; recorded as a decimal/time combination (see above).
* `project`: A string (up to 8 characters long) for identify the project to charge against.

## Use
### Initializing a time-tracking database
To set up a time-tracking database, one must have mysql (currently 5.7.15) installed locally on their machine. Then, they execute the `create.sql` script to initialize the database `timekeeper` with the table `timesheet` and an initial test entry.
