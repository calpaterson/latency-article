--- copy out all distinct hosts to a csv file
--- for now just exclude hosts that didn't get the mozilla page
\copy (select distinct host from accesslog where url = '/mozilla.html' order by host) to STDOUT with csv header;
