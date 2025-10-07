
create table dances (id int generated always as identity primary key, name varchar, keywords varchar, url varchar);
create table progress (username varchar, id int, status int);
create table interest (username varchar, id int, interest int);
