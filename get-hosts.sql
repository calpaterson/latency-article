--- copy out all distinct hosts to a csv file
\copy (select distinct host from accesslog order by host) to 'hosts.csv' with csv header;
