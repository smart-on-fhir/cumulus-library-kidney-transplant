create or replace view irae__rx_immunosuppressive as 
 select 'rx_immunosuppressive_drugs' as subtype, system, code, display from 
 irae__rx_immunosuppressive_drugs
 UNION select 'rx_immunosuppressive_systemic_therapy' as subtype, system, code, display from 
 irae__rx_immunosuppressive_systemic_therapy
 UNION select 'rx_immunosuppressive_immune_modulators' as subtype, system, code, display from 
 irae__rx_immunosuppressive_immune_modulators