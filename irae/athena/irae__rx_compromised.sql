create or replace view irae__rx_compromised as 
 select 'rx_compromised_therapies' as subtype, system, code, display from 
 irae__rx_compromised_therapies