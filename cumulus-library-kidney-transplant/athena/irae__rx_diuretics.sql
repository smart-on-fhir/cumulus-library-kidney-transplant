create or replace view irae__rx_diuretics as 
 select 'rx_diuretics_loop' as subtype, system, code, display from 
 irae__rx_diuretics_loop
 UNION select 'rx_diuretics_potassium' as subtype, system, code, display from 
 irae__rx_diuretics_potassium
 UNION select 'rx_diuretics_thiazide' as subtype, system, code, display from 
 irae__rx_diuretics_thiazide