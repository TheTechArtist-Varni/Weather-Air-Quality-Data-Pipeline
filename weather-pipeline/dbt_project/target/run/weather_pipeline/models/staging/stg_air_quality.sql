
  
  create view "warehouse"."main_staging"."stg_air_quality__dbt_tmp" as (
    select
    city,
    ts,
    pm10   as pm10_ugm3,
    pm2_5  as pm25_ugm3,
    us_aqi as aqi
from "warehouse"."main"."raw_air_quality"
where us_aqi is not null or pm2_5 is not null
  );
