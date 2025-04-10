create or replace view irae__lab_custom as 
 select 'lab_insulin' as valueset, system, code, display from 
 irae__lab_insulin
 UNION select 'lab_gad' as valueset, system, code, display from 
 irae__lab_gad
 UNION select 'lab_tacrolimus' as valueset, system, code, display from 
 irae__lab_tacrolimus
 UNION select 'lab_sirolimus' as valueset, system, code, display from 
 irae__lab_sirolimus
 UNION select 'lab_cyclosporin' as valueset, system, code, display from 
 irae__lab_cyclosporin
 UNION select 'lab_albumin_urine' as valueset, system, code, display from 
 irae__lab_albumin_urine
 UNION select 'lab_mycophenolate' as valueset, system, code, display from 
 irae__lab_mycophenolate
 UNION select 'lab_cytomegalovirus' as valueset, system, code, display from 
 irae__lab_cytomegalovirus
 UNION select 'lab_glucose' as valueset, system, code, display from 
 irae__lab_glucose
 UNION select 'lab_triglyceride' as valueset, system, code, display from 
 irae__lab_triglyceride
 UNION select 'lab_hemoglobin_a1c' as valueset, system, code, display from 
 irae__lab_hemoglobin_a1c
 UNION select 'lab_azathioprine' as valueset, system, code, display from 
 irae__lab_azathioprine
 UNION select 'lab_ldl' as valueset, system, code, display from 
 irae__lab_ldl
 UNION select 'lab_azathioprine_tpmt_gene' as valueset, system, code, display from 
 irae__lab_azathioprine_tpmt_gene
 UNION select 'lab_c_peptide' as valueset, system, code, display from 
 irae__lab_c_peptide
 UNION select 'lab_ketone_urine' as valueset, system, code, display from 
 irae__lab_ketone_urine
 UNION select 'lab_hdl' as valueset, system, code, display from 
 irae__lab_hdl