
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city
from "warehouse"."main_staging"."stg_air_quality"
where city is null



  
  
      
    ) dbt_internal_test