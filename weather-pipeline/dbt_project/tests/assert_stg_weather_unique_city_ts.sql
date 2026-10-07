-- Fails if any (city, ts) appears more than once.
select city, ts, count(*) as n
from {{ ref('stg_weather') }}
group by city, ts
having count(*) > 1
