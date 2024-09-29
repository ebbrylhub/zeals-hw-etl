-- 1. **Find the total number of trips for each day.**
SELECT date, COUNT(trip_id) AS total_trips_daily
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY 1 ASC;

-- 2. **Calculate the average trip duration for each day.**
SELECT date, ROUND(AVG(duration_minutes), 3) AS average_trip_duration_daily
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY 1 ASC;

-- 3. **Identify the top 5 stations with the highest number of trip starts.**
SELECT start_station_name, COUNT(trip_id) number_of_trip, COUNT(DISTINCT trip_id) AS unique_trip
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5;

-- 4. **Find the average number of trips per hour of the day.**
SELECT date, ROUND(COUNT(trip_id)/24, 2) AS average_number_of_trips_per_hour_of_day
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY 1 DESC;

-- 5. **Determine the most common trip route (start station to end station).**
SELECT start_station_name, end_station_name, COUNT(trip_id) total_trips
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1, 2
ORDER BY total_trips DESC
LIMIT 1;

-- 6. **Calculate the number of trips each month.**
SELECT DATE_TRUNC(date, month) AS month_key, COUNT(trip_id) AS number_of_trips 
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY 1;

-- 7. **Find the station with the longest average trip duration.**
SELECT start_station_name, end_station_name, AVG(duration_minutes) average_trip_duration
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1, 2
ORDER BY average_trip_duration DESC
LIMIT 1;

-- 8. **Find the busiest hour of the day (most trips started).**
SELECT hour, COUNT(trip_id) AS number_of_trips 
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY number_of_trips DESC;

-- 9. **Identify the day with the highest number of trips.**
SELECT date, COUNT(trip_id) AS number_of_trips
FROM `temporal-sweep-436906-n8.analytics.bikeshare_table`
GROUP BY 1
ORDER BY number_of_trips
LIMIT 1;