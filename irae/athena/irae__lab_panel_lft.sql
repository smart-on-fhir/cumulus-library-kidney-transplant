create or replace view irae__lab_panel_lft as 
 select 'lab_panel_lft_hepatic_function' as subtype, system, code, display from 
 irae__lab_panel_lft_hepatic_function