
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hours_observed
from "warehouse"."main_marts"."daily_city_metrics"
where hours_observed is null



  
  
      
    ) dbt_internal_test