create or replace view irae__dx_transplant as 
 select 'dx_transplant_kidney' as subtype, system, code, display from 
 irae__dx_transplant_kidney
 UNION select 'dx_transplant_solid_organ' as subtype, system, code, display from 
 irae__dx_transplant_solid_organ
 UNION select 'dx_transplant_recipient' as subtype, system, code, display from 
 irae__dx_transplant_recipient