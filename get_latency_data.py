#!/usr/bin/env python

import re
import csv
import sys
import requests
import json

MAX_CITY_ID = 800

def build_url():
    city_ids = ",".join(str(x) for x in range(MAX_CITY_ID))
    return f"https://wondernetwork.com/ping-data?sources={city_ids}&destinations={city_ids}"


latency_match = re.compile(r"\d+(\.\d+)?")

def main():
    url = build_url()
    print(url, file=sys.stderr)
    response = requests.get(url)
    response_body = response.json()
    csv_out = csv.DictWriter(
        sys.stdout,
        ["from", "to", "min", "max", "avg"],
        dialect="unix"
    )
    csv_out.writeheader()
    for from_id, from_data in response_body["pingData"].items():
        for to_id, data in from_data.items():
            if from_id == to_id:
                continue
            try:
                matches = [latency_match.match(x) for x in [data["min"], data["max"], data["avg"]]]
            except TypeError:
                print(f"unable to read {data}", file=sys.stderr)
                continue
            if None in matches:
                print(f"unable to read {data}", file=sys.stderr)
                continue
            csv_out.writerow({
                "from": data["source_name"],
                "to": data["destination_name"],
                "min": data["min"],
                "max": data["max"],
                "avg": data["avg"]
            })

if __name__ == "__main__":
    main()
