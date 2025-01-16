create or replace view irae__dx_compromised as 
 select 'dx_compromised_immunocompromised' as valueset, system, code, display from 
 irae__dx_compromised_immunocompromised
 UNION select 'dx_compromised_immunocompromising' as valueset, system, code, display from 
 irae__dx_compromised_immunocompromising