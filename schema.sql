CREATE TABLE IF NOT EXISTS accesslog (
id serial primary key,
host inet not null,
ident text not null,
username text not null,
time timestamptz not null,
verb text not null,
url text not null,
httpver text not null,
status int not null,
size int not null,
referer text not null,
useragent text not null
)
;
CREATE INDEX IF NOT EXISTS accesslog_host on accesslog (host);
CREATE INDEX IF NOT EXISTS accesslog_time on accesslog (time);
CREATE INDEX IF NOT EXISTS accesslog_verb on accesslog (verb);
CREATE INDEX IF NOT EXISTS accesslog_url on accesslog (url);

CREATE TABLE IF NOT EXISTS geocoded_hosts (
host inet primary key,
location geography not null,
accuracy_radius int not null
);
