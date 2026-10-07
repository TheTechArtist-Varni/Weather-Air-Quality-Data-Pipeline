
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Fails for any row with humidity outside 0-100 %.
select *
from "warehouse"."main_staging"."stg_weather"
where humidity_pct < 0 or humidity_pct > 100
  
  
      
    ) dbt_internal_test