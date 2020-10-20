#!/usr/bin/env python3

# accesslog2csv: Convert default, unified access log from Apache, Nginx
# servers to CSV format.
#
# Original source by Maja Kraljic, July 18, 2017
# Modified by Joshua Wright to parse all elements in the HTTP request as
# different columns, December 16, 2019

# Subsequent changes by Cal Paterson, Oct 2020:
# - skip log lines that don't match this regex (this is mostly roving bots trying to hack php)
# - output iso datetimes
# - work on streams
# - unix style csvs

import csv
import re
import sys
from datetime import datetime

NGINX_DATETIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

pattern = re.compile(r'(?P<host>\S+).(?P<rfc1413ident>\S+).(?P<username>\S+).\[(?P<datetime>\S+ \+[0-9]{4})]."(?P<httpverb>\S+) (?P<url>\S+) (?P<httpver>\S+)" (?P<status>[0-9]+) (?P<size>\S+) "(?P<referer>.*)" "(?P<useragent>.*)"\s*\Z')

if __name__ == "__main__":
    log_f = sys.stdin

    csv_out=csv.writer(sys.stdout, dialect="unix")
    csv_out.writerow(['host', 'ident', 'username', 'time', 'verb', 'url', 'httpver', 'status', 'size', 'referer', 'useragent'])

    for line in log_f:
        m = pattern.match(line)
        try:
            result = list(m.groups())
        except AttributeError:
            # I need this because of various bots trying it on with thonkphp nonsense - CJP
            # print("bad line = %s" % line, file=sys.stderr)
            continue
        result[3] = datetime.strptime(result[3], NGINX_DATETIME_FORMAT).isoformat()
        csv_out.writerow(result)
