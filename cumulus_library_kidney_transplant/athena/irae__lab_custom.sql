create or replace view irae__lab_custom as 
 select 'lab_lab_albumin_urine' as valueset, system, code, display from 
 irae__lab_lab_albumin_urine
 UNION ALL
select 'lab_lab_azathioprine' as valueset, system, code, display from 
 irae__lab_lab_azathioprine
 UNION ALL
select 'lab_lab_azathioprine_tpmt_gene' as valueset, system, code, display from 
 irae__lab_lab_azathioprine_tpmt_gene
 UNION ALL
select 'lab_lab_c_peptide' as valueset, system, code, display from 
 irae__lab_lab_c_peptide
 UNION ALL
select 'lab_lab_cyclosporin' as valueset, system, code, display from 
 irae__lab_lab_cyclosporin
 UNION ALL
select 'lab_lab_cytomegalovirus' as valueset, system, code, display from 
 irae__lab_lab_cytomegalovirus
 UNION ALL
select 'lab_lab_gad' as valueset, system, code, display from 
 irae__lab_lab_gad
 UNION ALL
select 'lab_lab_gfr_custom' as valueset, system, code, display from 
 irae__lab_lab_gfr_custom
 UNION ALL
select 'lab_lab_glucose' as valueset, system, code, display from 
 irae__lab_lab_glucose
 UNION ALL
select 'lab_lab_hdl' as valueset, system, code, display from 
 irae__lab_lab_hdl
 UNION ALL
select 'lab_lab_hemoglobin_a1c' as valueset, system, code, display from 
 irae__lab_lab_hemoglobin_a1c
 UNION ALL
select 'lab_lab_hla' as valueset, system, code, display from 
 irae__lab_lab_hla
 UNION ALL
select 'lab_lab_insulin' as valueset, system, code, display from 
 irae__lab_lab_insulin
 UNION ALL
select 'lab_lab_ketone_urine' as valueset, system, code, display from 
 irae__lab_lab_ketone_urine
 UNION ALL
select 'lab_lab_ldl' as valueset, system, code, display from 
 irae__lab_lab_ldl
 UNION ALL
select 'lab_lab_mycophenolate' as valueset, system, code, display from 
 irae__lab_lab_mycophenolate
 UNION ALL
select 'lab_lab_sirolimus' as valueset, system, code, display from 
 irae__lab_lab_sirolimus
 UNION ALL
select 'lab_lab_tacrolimus' as valueset, system, code, display from 
 irae__lab_lab_tacrolimus
 UNION ALL
select 'lab_lab_triglyceride' as valueset, system, code, display from 
 irae__lab_lab_triglyceride