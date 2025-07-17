create or replace view irae__dx_transplant as 
 select 'dx_transplant_kidney' as valueset, system, code, display from 
 irae__dx_transplant_kidney