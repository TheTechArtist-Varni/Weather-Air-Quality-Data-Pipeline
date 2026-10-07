-- Fails for any row with humidity outside 0-100 %.
select *
from {{ ref('stg_weather') }}
where humidity_pct < 0 or humidity_pct > 100
