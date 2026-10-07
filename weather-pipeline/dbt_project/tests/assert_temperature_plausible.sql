-- Fails for physically implausible temperatures (deg C).
select *
from {{ ref('stg_weather') }}
where temperature_c < -60 or temperature_c > 60
