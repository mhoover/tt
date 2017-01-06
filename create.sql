create database timekeeper;
use timekeeper;
create table timesheet (
    id int not null auto_increment,
    date varchar(10),
    start decimal(4, 2),
    end decimal(4, 2),
    project varchar(8),
    primary key (id)
);
insert into timesheet (date, start, end, project) values ('01/01/2016', 0, 1, 'test');
