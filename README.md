# Scratchings for a latency article

This repo contains the code/data for the article ["Where's the fastest place to
put my server? How much does it matter?"](https://calpaterson.com/latency.html)
on my website.

## Building

Requirements:

1. postgres
2. a database called `latency`
3. postgis extension installed in that database
4. Python 3
5. the packages in the [requirements.txt](requirements.txt)
   - the shapely wheel doesn't get on with libgeos on debian stable, so I had
     to use the following magic incantation: `pip install shapely --no-binary
     shapely`
6. Maxmind's "GeoLite2 City" database file, `GeoLite2-City.mmdb`
7. A few C libraries, the debian packages for which are:
   - libgeos-dev
   - libproj-dev

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
- [get-connectedness.sql](get-connectedness.sql) - query to get internet speeds vs speed of light
