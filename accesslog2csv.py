# accesslog2csv: Convert default, unified access log from Apache, Nginx
# servers to CSV format.
#
# Original source by Maja Kraljic, July 18, 2017
# Modified by Joshua Wright to parse all elements in the HTTP request as
# different columns, December 16, 2019


import csv
import re
import sys

if len(sys.argv) == 1:
    sys.stdout.write("Usage: %s <access.log> <accesslog.csv>\n"%sys.argv[0])
    sys.exit(0)

log_file_name = sys.argv[1]
csv_file_name = sys.argv[2]

pattern = re.compile(r'(?P<host>\S+).(?P<rfc1413ident>\S+).(?P<user>\S+).\[(?P<datetime>\S+ \+[0-9]{4})]."(?P<httpverb>\S+) (?P<url>\S+) (?P<httpver>\S+)" (?P<status>[0-9]+) (?P<size>\S+) "(?P<referer>.*)" "(?P<useragent>.*)"\s*\Z')

file = open(log_file_name)

with open(csv_file_name, 'w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['host', 'ident', 'user', 'time', 'verb', 'url', 'httpver', 'status', 'size', 'referer', 'useragent'])

    for line in file:
        m = pattern.match(line)
        result = m.groups()
        csv_out.writerow(result)
