all: concat.csv schema.sentinel hosts.csv

concat.csv: calpaterson-logs-2020-09-30/access.log accesslog2csv.py
	cat calpaterson-logs-2020-09-30/access.log* | python3 accesslog2csv.py > concat.csv

schema.sentinel: schema.sql
	psql -d latency -1 -f schema.sql
	touch schema.sentinel

accesslog-load.sentinel: concat.csv load-accesslog.sql
	psql -d latency -1 -f load-accesslog.sql
	touch load-accesslog.sentinel

hosts.csv: get-hosts.sql accesslog-load.sentinel
	psql -d latency -1 -f get-hosts.sql
