#!/usr/bin/env python3

"""Geocode the set of host ips"""

import csv
import sys

import geoip2.database

def main():
    csv_out = csv.writer(
        sys.stdout,
        dialect="unix"
    )
    csv_in = csv.reader(sys.stdin)
    csv_out.writerow(["host", "latlng_wkt", "accuracy_radius"])
    next(csv_in) # skip header

    with geoip2.database.Reader("GeoLite2-City.mmdb") as mmdb:
        # FIXME: Consider checking anonymous proxies here
        for host, in csv_in:
            ip_info = mmdb.city(host)
            try:
                lat = int(ip_info.location.latitude)
                lng = int(ip_info.location.longitude)
                accuracy_radius = int(ip_info.location.accuracy_radius)
            except TypeError:
                print(f"unable to geocode ip: {ip_info}", file=sys.stderr)
                continue
            point_wkt = f"SRID=4326; POINT( {lng} {lat})"
            csv_out.writerow([host, point_wkt, accuracy_radius])

if __name__ == "__main__":
    main()

