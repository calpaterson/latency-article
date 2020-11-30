-- This query gets the latencies from London to other cities with more than 5m
-- people, along with the slowdown factor compared to the speed of light.
SELECT
latencies.to_ as to_,
round(ST_Distance(from_cities.location, to_cities.location) / 1000) as distance_km,
round(latencies.avg) as internet_latency,
round(ST_Distance(from_cities.location, to_cities.location) / 299792) as  speed_of_light_latency,
round((latencies.avg / (ST_Distance(from_cities.location, to_cities.location) / 299792))::numeric, 1) as slowdown_factor
FROM latencies
JOIN geocoded_cities as geo_to_cities on geo_to_cities.latency_city_name = latencies.to_
JOIN cities as to_cities on geo_to_cities.geoname_id = to_cities.geoname_id
JOIN geocoded_cities as geo_from_cities on geo_from_cities.latency_city_name = latencies.from_
JOIN cities as from_cities on geo_from_cities.geoname_id = from_cities.geoname_id
WHERE latencies.from_ = 'London'
AND to_cities.population > 5000000
ORDER by slowdown_factor asc;
