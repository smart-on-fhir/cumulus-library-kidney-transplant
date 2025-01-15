create or replace view irae__lab_custom as 
 select 'lab_hemoglobin_a1c' as subtype, system, code, display from 
 irae__lab_hemoglobin_a1c
 UNION select 'lab_cytomegalovirus' as subtype, system, code, display from 
 irae__lab_cytomegalovirus
 UNION select 'lab_cyclosporin' as subtype, system, code, display from 
 irae__lab_cyclosporin
 UNION select 'lab_mycophenolate' as subtype, system, code, display from 
 irae__lab_mycophenolate
 UNION select 'lab_sirolimus' as subtype, system, code, display from 
 irae__lab_sirolimus
 UNION select 'lab_azathioprine' as subtype, system, code, display from 
 irae__lab_azathioprine
 UNION select 'lab_azathioprine_tpmt_gene' as subtype, system, code, display from 
 irae__lab_azathioprine_tpmt_gene
 UNION select 'lab_tacrolimus' as subtype, system, code, display from 
 irae__lab_tacrolimus