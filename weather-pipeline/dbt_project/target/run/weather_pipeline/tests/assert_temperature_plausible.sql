
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Fails for physically implausible temperatures (deg C).
select *
from "warehouse"."main_staging"."stg_weather"
where temperature_c < -60 or temperature_c > 60
  
  
      
    ) dbt_internal_test