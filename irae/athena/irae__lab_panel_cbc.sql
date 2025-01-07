create or replace view irae__lab_panel_cbc as 
 select 'lab_panel_cbc_with_diff' as subtype, system, code, display from 
 irae__lab_panel_cbc_with_diff