-- Load outputs/indicator_observations.csv as indicator_observations.
-- Keep observation year: the latest observation may vary by series/country.
SELECT country, indicator, MIN(year) AS first_year, MAX(year) AS last_year,
       COUNT(*) AS observed_years
FROM indicator_observations
GROUP BY country, indicator ORDER BY indicator, country;

SELECT country, year, value AS youth_unemployment_pct
FROM indicator_observations
WHERE indicator_code = 'SL.UEM.1524.ZS' AND year >= 2015
ORDER BY country, year;

SELECT country, year, value AS internet_users_pct
FROM indicator_observations
WHERE indicator_code = 'IT.NET.USER.ZS' AND year >= 2015
ORDER BY country, year;
