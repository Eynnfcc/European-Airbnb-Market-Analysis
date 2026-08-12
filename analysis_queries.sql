-- =========================================================
-- AIRBNB PRICES IN EUROPEAN CITIES
-- GOLD LAYER - SQL ANALYSIS
-- =========================================================


-- ---------------------------------------------------------
-- 1. AVERAGE AIRBNB PRICE BY CITY
-- ---------------------------------------------------------

SELECT
    c.city,
    COUNT(*) AS total_listings,
    ROUND(AVG(f.realsum), 2) AS average_price
FROM fact_airbnb AS f
JOIN dim_city AS c
    ON f.city_id = c.city_id
GROUP BY c.city
ORDER BY average_price DESC;


-- ---------------------------------------------------------
-- 2. WEEKDAY VS WEEKEND ANALYSIS
-- ---------------------------------------------------------

SELECT
    d.day_type,
    COUNT(*) AS total_listings,
    ROUND(AVG(f.realsum), 2) AS average_price,
    ROUND(AVG(f.guest_satisfaction_overall), 2) AS average_satisfaction
FROM fact_airbnb AS f
JOIN dim_day_type AS d
    ON f.day_type_id = d.day_type_id
GROUP BY d.day_type
ORDER BY average_price DESC;


-- ---------------------------------------------------------
-- 3. ROOM TYPE ANALYSIS
-- ---------------------------------------------------------

SELECT
    r.room_type,
    COUNT(*) AS total_listings,
    ROUND(AVG(f.realsum), 2) AS average_price,
    ROUND(AVG(f.guest_satisfaction_overall), 2) AS average_satisfaction
FROM fact_airbnb AS f
JOIN dim_room_type AS r
    ON f.room_type_id = r.room_type_id
GROUP BY r.room_type
ORDER BY average_price DESC;