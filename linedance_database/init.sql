create table dances (id int generated always as identity primary key, name varchar, keywords varchar, url varchar);
create table progress (username varchar, id int, status int, foreign key (id) references dances(id) on delete cascade); -- NOTE: should have primary key
create table interest (username varchar, id int, interest int, foreign key (id) references dances(id) on delete cascade); -- NOTE: should have primary key
create table dance_descriptions (id int primary key, description varchar, foreign key (id) references dances(id) on delete cascade);
