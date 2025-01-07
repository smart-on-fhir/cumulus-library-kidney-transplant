create or replace view irae__lab_panel_cmp as 
 select 'lab_panel_cmp_comprehensive' as subtype, system, code, display from 
 irae__lab_panel_cmp_comprehensive