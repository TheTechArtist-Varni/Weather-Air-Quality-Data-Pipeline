-- Fails for physically implausible temperatures (deg C).
select *
from "warehouse"."main_staging"."stg_weather"
where temperature_c < -60 or temperature_c > 60