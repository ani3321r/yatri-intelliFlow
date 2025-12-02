-- Namma Yatri Analytics - Core SQL Queries
-- Assumes table: rides

-- 1. Peak hours by total rides
SELECT
    hour_of_day,
    COUNT(*) AS total_rides
FROM rides
GROUP BY hour_of_day
ORDER BY total_rides DESC;

-- 2. Peak hours by completed rides
SELECT
    hour_of_day,
    COUNT(*) AS completed_rides
FROM rides
WHERE is_completed = 1
GROUP BY hour_of_day
ORDER BY completed_rides DESC;

-- 3. Top pickup zones by revenue
SELECT
    pickup_zone,
    SUM(fare_amount) AS total_revenue,
    COUNT(*) AS total_rides
FROM rides
WHERE is_completed = 1
GROUP BY pickup_zone
ORDER BY total_revenue DESC;

-- 4. Cancellation rate by hour
SELECT
    hour_of_day,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) AS cancelled_rides,
    ROUND(
        100.0 * SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS cancellation_rate_pct
FROM rides
GROUP BY hour_of_day
ORDER BY cancellation_rate_pct DESC;

-- 5. Cancellation rate by pickup zone
SELECT
    pickup_zone,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) AS cancelled_rides,
    ROUND(
        100.0 * SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS cancellation_rate_pct
FROM rides
GROUP BY pickup_zone
ORDER BY cancellation_rate_pct DESC;

-- 6. Driver performance summary
SELECT
    driver_id,
    COUNT(*) AS total_rides,
    SUM(is_completed) AS completed_rides,
    ROUND(
        100.0 * SUM(is_completed) / COUNT(*),
        2
    ) AS completion_rate_pct,
    SUM(CASE WHEN is_completed = 1 THEN fare_amount ELSE 0 END) AS total_revenue,
    ROUND(AVG(NULLIF(rating, '')), 2) AS avg_rating
FROM rides
GROUP BY driver_id
ORDER BY total_revenue DESC;

-- 7. Zone-to-zone flow (top OD pairs)
SELECT
    pickup_zone,
    drop_zone,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN is_completed = 1 THEN fare_amount ELSE 0 END) AS total_revenue
FROM rides
GROUP BY pickup_zone, drop_zone
ORDER BY total_rides DESC
LIMIT 20;

-- 8. Revenue by day of week
SELECT
    day_of_week,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN is_completed = 1 THEN fare_amount ELSE 0 END) AS total_revenue
FROM rides
GROUP BY day_of_week
ORDER BY total_revenue DESC;

-- 9. Wait time impact on cancellations
SELECT
    CASE
        WHEN wait_time_min < 3 THEN '<3 min'
        WHEN wait_time_min BETWEEN 3 AND 5 THEN '3-5 min'
        WHEN wait_time_min BETWEEN 6 AND 8 THEN '6-8 min'
        ELSE '>8 min'
    END AS wait_bucket,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) AS cancelled_rides,
    ROUND(
        100.0 * SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS cancellation_rate_pct
FROM rides
GROUP BY wait_bucket
ORDER BY cancellation_rate_pct DESC;

-- 10. Average fare and distance by zone
SELECT
    pickup_zone,
    ROUND(AVG(distance_km), 2) AS avg_distance_km,
    ROUND(AVG(fare_amount), 2) AS avg_fare
FROM rides
WHERE is_completed = 1
GROUP BY pickup_zone
ORDER BY avg_fare DESC;

-- 11. High-value customers (by total spend)
SELECT
    rider_id,
    COUNT(*) AS total_rides,
    SUM(CASE WHEN is_completed = 1 THEN fare_amount ELSE 0 END) AS total_spend
FROM rides
GROUP BY rider_id
HAVING total_spend > 2000
ORDER BY total_spend DESC;

-- 12. Time-based revenue trend (by hour)
SELECT
    hour_of_day,
    SUM(CASE WHEN is_completed = 1 THEN fare_amount ELSE 0 END) AS total_revenue
FROM rides
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- 13. Zone-level KPI summary
SELECT
    pickup_zone,
    COUNT(*) AS total_rides,
    SUM(is_completed) AS completed_rides,
    ROUND(
        100.0 * SUM(is_completed) / COUNT(*),
        2
    ) AS completion_rate_pct,
    SUM(CASE WHEN is_completed = 1 THEN fare_amount ELSE 0 END) AS total_revenue,
    ROUND(AVG(distance_km), 2) AS avg_distance_km,
    ROUND(AVG(wait_time_min), 2) AS avg_wait_time_min
FROM rides
GROUP BY pickup_zone
ORDER BY total_revenue DESC;


