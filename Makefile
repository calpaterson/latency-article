concat.csv: calpaterson-logs-2020-09-30/access.log accesslog2csv.py
	cat calpaterson-logs-2020-09-30/access.log* | python3 accesslog2csv.py > concat.csv
