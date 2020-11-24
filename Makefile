all: concat.csv schema.sentinel hosts.csv geocoded-hosts.csv

concat.csv: calpaterson-logs-2020-09-30/access.log accesslog2csv.py
	cat calpaterson-logs-2020-09-30/access.log* | python3 accesslog2csv.py > concat.csv

schema.sentinel: schema.sql
	psql -d latency -1 -f schema.sql
	touch schema.sentinel

accesslog-load.sentinel: load-accesslog.sql schema.sentinel calpaterson-logs-2020-09-30/access.log accesslog2csv.py
	cat calpaterson-logs-2020-09-30/access.log* | ./accesslog2csv.py | psql -d latency -1 -f "$(file < load-accesslog.sql)"
	touch load-accesslog.sentinel

# This is slow so a sep target
geocoded-hosts.csv: host_latlngs.py accesslog-load.sentinel schema.sentinel
	psql -d latency -1 -f get-hosts.sql | ./host_latlngs.py > geocoded-hosts.csv

geocoded-hosts-load.sentinel: geocoded-hosts.csv load-geocoded-hosts.sql schema.sentinel
	cat geocoded-hosts.csv | psql -d latency -1 -c "$(file < load-geocoded-hosts.sql)"
	touch geocoded-hosts-load.sentinel

cities-load.sentinel: schema.sentinel cities15000.txt
	cat cities15000.txt | ./cities_2_wkt.py | psql -d latency -1 -c "$(file < load-cities.sql)"
	touch cities-load.sentinel

latencies-load.sentinel: schema.sentinel latency-matrix.csv
	cat latency-matrix.csv | psql -d latency -1 -c "$(file < load-latencies.sql)"
	touch latencies-load.sentinel

# External data sources
#
latency-matrix.csv: get-latency-data.py
	./get-wondernetwork-data.py > latency-matrix.csv

cities15000.txt:
	wget http://download.geonames.org/export/dump/cities15000.zip
	unzip cities15000.zip
