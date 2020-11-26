-- This query tries to geocode by name as far as possible based on string
-- match...the rest will be manual

\copy ( SELECT latency_cities.name as latency_city_name, cities.name geonames_city_name, geoname_id, population, country_code, ST_X(location::geometry) || ' ' || ST_Y(location::geometry) as location, count(*) OVER (PARTITION BY latency_cities.name) FROM (      SELECT from_ as name from latencies      UNION SELECT to_ as city_name from latencies ) as latency_cities LEFT JOIN cities USING(name) ) TO 'geocoded-cities.csv' WITH CSV HEADER ;
