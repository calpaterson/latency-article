# Scratchings for a latency article

This repo contains the code/data for the latency article on my website.

## Building

Requirements:

1. postgres
2. a database called `latency`
3. postgis extension installed in that database
4. Python 3
5. the packages in the [requirements.txt](requirements.txt)
6. Maxmind's "GeoLite2 City" database file, `GeoLite2-City.mmdb`

Then run:

```
make -j
```

If you just want to see what I did, best to read the [makefile](Makefile) directly.

## Files

- [geocoded-cities.csv](geocoded-cities.csv) - my, **hand corrected**,
  geocoding of Wonder Network city names (except "Koto", "Malaysia", "Mexico"
  and "Monticello" - which I can't narrow down) to Geoname's geoid
- [partial-geocode.sql](partial-geocode.sql) - query I used to extract data to create the above
