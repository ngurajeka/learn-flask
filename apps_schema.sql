drop table if exists team;
create table team (
	id integer primary key autoincrement,
	username text not null,
	firstname text not null,
	lastname text not null,
	avatar text null,
	role text not null
);
