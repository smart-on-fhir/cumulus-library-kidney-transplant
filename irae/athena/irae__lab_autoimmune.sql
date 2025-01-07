create or replace view irae__lab_autoimmune as 
 select 'lab_autoimmune_serum_rf' as subtype, system, code, display from 
 irae__lab_autoimmune_serum_rf
 UNION select 'lab_autoimmune_blood_esr' as subtype, system, code, display from 
 irae__lab_autoimmune_blood_esr
 UNION select 'lab_autoimmune_crp' as subtype, system, code, display from 
 irae__lab_autoimmune_crp
 UNION select 'lab_autoimmune_tsh' as subtype, system, code, display from 
 irae__lab_autoimmune_tsh
 UNION select 'lab_autoimmune_t3' as subtype, system, code, display from 
 irae__lab_autoimmune_t3
 UNION select 'lab_autoimmune_t4' as subtype, system, code, display from 
 irae__lab_autoimmune_t4