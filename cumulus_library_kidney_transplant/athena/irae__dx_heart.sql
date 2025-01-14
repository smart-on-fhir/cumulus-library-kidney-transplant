create or replace view irae__dx_heart as 
 select 'dx_heart_cardiomyopathy' as subtype, system, code, display from 
 irae__dx_heart_cardiomyopathy
 UNION select 'dx_heart_attack' as subtype, system, code, display from 
 irae__dx_heart_attack
 UNION select 'dx_heart_failure' as subtype, system, code, display from 
 irae__dx_heart_failure
 UNION select 'dx_heart_cohort' as subtype, system, code, display from 
 irae__dx_heart_cohort