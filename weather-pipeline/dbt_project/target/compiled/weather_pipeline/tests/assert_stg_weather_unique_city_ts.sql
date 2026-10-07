-- Fails if any (city, ts) appears more than once.
select city, ts, count(*) as n
from "warehouse"."main_staging"."stg_weather"
group by city, ts
having count(*) > 1