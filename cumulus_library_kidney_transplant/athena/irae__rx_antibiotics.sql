create or replace view irae__rx_antibiotics as 
 select 'rx_antibiotics_any' as subtype, system, code, display from 
 irae__rx_antibiotics_any
 UNION select 'rx_antibiotics_systemic' as subtype, system, code, display from 
 irae__rx_antibiotics_systemic