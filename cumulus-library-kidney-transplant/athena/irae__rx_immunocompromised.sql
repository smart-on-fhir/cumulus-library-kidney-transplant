create or replace view irae__rx_immunocompromised as 
 select 'rx_immunocompromised_therapies' as subtype, system, code, display from 
 irae__rx_immunocompromised_therapies