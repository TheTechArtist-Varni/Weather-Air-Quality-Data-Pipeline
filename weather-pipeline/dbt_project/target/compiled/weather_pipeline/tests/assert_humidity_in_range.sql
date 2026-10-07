-- Fails for any row with humidity outside 0-100 %.
select *
from "warehouse"."main_staging"."stg_weather"
where humidity_pct < 0 or humidity_pct > 100