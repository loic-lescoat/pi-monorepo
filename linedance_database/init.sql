create table dances (id int generated always as identity primary key, name varchar, keywords varchar, url varchar);
create table progress (username varchar, id int, status int, foreign key (id) references dances(id) on delete cascade); -- NOTE: should have primary key
create table interest (username varchar, id int, interest int, foreign key (id) references dances(id) on delete cascade); -- NOTE: should have primary key
create table dance_descriptions (id int primary key, description varchar,
  -- rows that follow are surmised from description column
  dance_name varchar,
  song_name varchar,
  song_artist varchar,
  counts varchar, -- keeping as varchar just in case is not int in all cases
  foreign key (id) references dances(id) on delete cascade);
