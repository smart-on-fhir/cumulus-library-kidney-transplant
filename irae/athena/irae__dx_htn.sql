create or replace view irae__dx_htn as 
 select 'dx_htn_essential' as subtype, system, code, display from 
 irae__dx_htn_essential
 UNION select 'dx_htn_any' as subtype, system, code, display from 
 irae__dx_htn_any
 UNION select 'dx_htn_hypertensive_ckd' as subtype, system, code, display from 
 irae__dx_htn_hypertensive_ckd