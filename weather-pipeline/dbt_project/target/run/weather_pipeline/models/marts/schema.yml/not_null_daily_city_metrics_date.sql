
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date
from "warehouse"."main_marts"."daily_city_metrics"
where date is null



  
  
      
    ) dbt_internal_test