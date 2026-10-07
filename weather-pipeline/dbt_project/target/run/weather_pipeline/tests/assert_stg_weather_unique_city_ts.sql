
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Fails if any (city, ts) appears more than once.
select city, ts, count(*) as n
from "warehouse"."main_staging"."stg_weather"
group by city, ts
having count(*) > 1
  
  
      
    ) dbt_internal_test