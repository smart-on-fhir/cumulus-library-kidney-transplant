create or replace view irae__lab_lft as 
 select 'lab_lft_function' as subtype, system, code, display from 
 irae__lab_lft_function
 UNION select 'lab_lft_ggt' as subtype, system, code, display from 
 irae__lab_lft_ggt
 UNION select 'lab_lft_pt' as subtype, system, code, display from 
 irae__lab_lft_pt
 UNION select 'lab_lft_inr' as subtype, system, code, display from 
 irae__lab_lft_inr