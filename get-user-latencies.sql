--- This query returns the data for the main table in the article: latency
--- percentiles as if my server was located in each of the cities I have
--- latency data for

SELECT
t.city_name,
round(percentile_disc(0.5) within group (order by t.latency)) as p50,
round(percentile_disc(0.75) within group (order by t.latency)) as p75,
round(percentile_disc(0.99) within group (order by t.latency)) as p99
FROM (
SELECT
latencies.from_ as city_name,
avg as latency
FROM
geocoded_hosts
CROSS JOIN LATERAL (
     SELECT cities.geoname_id, cities.location
     FROM cities
     ORDER BY geocoded_hosts.location <-> cities.location
     LIMIT 1
) as closest_cities
JOIN geocoded_cities ON closest_cities.geoname_id = geocoded_cities.geoname_id
JOIN accesslog USING (host)
CROSS JOIN latencies
WHERE accesslog.useragent like 'Mozilla%'
) as t
group by t.city_name
order by p99;
