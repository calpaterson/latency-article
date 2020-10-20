\copy accesslog (host, ident, username, time, verb, url, httpver, status, size, referer, useragent) from 'concat.csv' with csv header;
