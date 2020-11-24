#!/usr/bin/env python3

"""Pre-process the cities15000.txt file (mostly to use WKT)"""

import csv
import sys

def main():
    csv_out = csv.DictWriter(
        sys.stdout,
        [
            "geoname_id",
            "name",
            "ascii_name",
            "location",
            "country_code",
            "population",
        ],
        dialect="unix"
    )

    # See here for field descriptions:
    # http://download.geonames.org/export/dump/readme.txt
    csv_in = csv.DictReader(
        sys.stdin,
        [
            "geonameid",
            "name",
            "asciiname",
            "alternatenames",
            "latitude",
            "longitude",
            "feature class",
            "feature code",
            "country code",
            "cc2",
            "admin1 code",
            "admin2 code",
            "admin3 code",
            "admin4 code",
            "population",
            "elevation",
            "dem",
            "timezone",
            "modification date",
        ],
        dialect="excel-tab"
    )
    csv_out.writeheader()
    for row in csv_in:
        csv_out.writerow(dict(
            geoname_id=row["geonameid"],
            name=row["name"],
            ascii_name=row["asciiname"],
            location=f"SRID=4326; POINT( {row['longitude']} {row['latitude']})",
            country_code=row["country code"],
            population=row["population"],
        ))


if __name__ == "__main__":
    main()
