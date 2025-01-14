create or replace view irae__dx_compromised as 
 select 'dx_compromised_immunocompromised' as subtype, system, code, display from 
 irae__dx_compromised_immunocompromised
 UNION select 'dx_compromised_immunocompromising' as subtype, system, code, display from 
 irae__dx_compromised_immunocompromising