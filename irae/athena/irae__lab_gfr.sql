create or replace view irae__lab_gfr as 
 select 'lab_gfr_eGFR' as subtype, system, code, display from 
 irae__lab_gfr_eGFR