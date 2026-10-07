
    

    create  table
      "warehouse"."main_marts"."daily_city_metrics__dbt_tmp"
  
    
    as (
      with joined as (
    select
        w.city,
        cast(w.ts as date) as date,
        w.temperature_c,
        w.humidity_pct,
        w.precipitation_mm,
        w.wind_kmh,
        a.pm25_ugm3,
        a.aqi
    from "warehouse"."main_staging"."stg_weather" w
    left join "warehouse"."main_staging"."stg_air_quality" a
        on w.city = a.city and w.ts = a.ts
)

select
    city,
    date,
    round(avg(temperature_c), 1)  as avg_temp_c,
    max(temperature_c)            as max_temp_c,
    min(temperature_c)            as min_temp_c,
    round(avg(humidity_pct), 1)   as avg_humidity_pct,
    round(sum(precipitation_mm), 1) as total_precip_mm,
    round(avg(wind_kmh), 1)       as avg_wind_kmh,
    round(avg(pm25_ugm3), 1)      as avg_pm25_ugm3,
    max(aqi)                      as max_aqi,
    max(temperature_c) >= 35      as is_hot_day,
    case
        when max(aqi) is null then 'unknown'
        when max(aqi) <= 50  then 'good'
        when max(aqi) <= 100 then 'moderate'
        when max(aqi) <= 150 then 'unhealthy for sensitive groups'
        else 'unhealthy'
    end as aqi_category,
    count(*) as hours_observed
from joined
group by city, date
    );
    
  