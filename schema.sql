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

CREATE TABLE IF NOT EXISTS latencies (
       from_ text not null,
       to_ text not null,
       min double precision not null,
       max double precision not null,
       avg double precision not null,
       PRIMARY KEY (from_, to_)
);

CREATE INDEX IF NOT EXISTS latencies_avg on latencies (from_, to_, avg);

CREATE TABLE IF NOT EXISTS cities (
       geoname_id int primary key,
       name text not null,
       ascii_name text not null,
       location geography not null,
       country_code text not null,
       population bigint not null
);

CREATE TABLE IF NOT EXISTS geocoded_cities (
       latency_city_name text not null unique,
       geoname_id int primary key
)
