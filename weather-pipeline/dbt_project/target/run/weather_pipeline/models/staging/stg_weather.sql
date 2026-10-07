
  
  create view "warehouse"."main_staging"."stg_weather__dbt_tmp" as (
    select
    city,
    ts,
    temperature_2m      as temperature_c,
    relative_humidity_2m as humidity_pct,
    precipitation       as precipitation_mm,
    wind_speed_10m      as wind_kmh
from "warehouse"."main"."raw_weather"
where temperature_2m is not null
  );
