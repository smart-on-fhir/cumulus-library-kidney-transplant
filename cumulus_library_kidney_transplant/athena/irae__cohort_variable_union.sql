create table irae__cohort_variable_union as
with select_union as
(
	select 'dx_transplant'	 as variable, code, display, system, encounter_ref, condition_ref as resource_ref from irae__cohort_dx_transplant UNION ALL
	select 'lab_albumin'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_albumin UNION ALL
	select 'lab_crp'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_crp UNION ALL
	select 'lab_drug_level_azathioprine'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_drug_level_azathioprine UNION ALL
	select 'lab_drug_level_cyclosporin'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_drug_level_cyclosporin UNION ALL
	select 'lab_drug_level_mycophenolate'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_drug_level_mycophenolate UNION ALL
	select 'lab_drug_level_sirolimus'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_drug_level_sirolimus UNION ALL
	select 'lab_drug_level_tacrolimus'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_drug_level_tacrolimus UNION ALL
	select 'lab_esr'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_esr UNION ALL
	select 'lab_gfr_custom'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_gfr_custom UNION ALL
	select 'lab_hla'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_hla UNION ALL
	select 'lab_infection_viral_cmv'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_infection_viral_cmv UNION ALL
	select 'lab_iron_ferritin'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_iron_ferritin UNION ALL
	select 'lab_tpmt_gene'	 as variable, code, display, system, encounter_ref, observation_ref as resource_ref from irae__cohort_lab_tpmt_gene UNION ALL
	select 'proc_nephrectomy'	 as variable, code, display, system, encounter_ref, procedure_ref as resource_ref from irae__cohort_proc_nephrectomy UNION ALL
	select 'proc_transplant'	 as variable, code, display, system, encounter_ref, procedure_ref as resource_ref from irae__cohort_proc_transplant UNION ALL
	select 'rx_alemtuzumab'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_alemtuzumab UNION ALL
	select 'rx_atg'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_atg UNION ALL
	select 'rx_azathioprine'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_azathioprine UNION ALL
	select 'rx_basiliximab'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_basiliximab UNION ALL
	select 'rx_belatacept'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_belatacept UNION ALL
	select 'rx_cyclosporin'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_cyclosporin UNION ALL
	select 'rx_cytogam'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_cytogam UNION ALL
	select 'rx_everolimus'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_everolimus UNION ALL
	select 'rx_ig'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_ig UNION ALL
	select 'rx_ivig'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_ivig UNION ALL
	select 'rx_methylprednisolone'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_methylprednisolone UNION ALL
	select 'rx_mycophenolate'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_mycophenolate UNION ALL
	select 'rx_prednisolone'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_prednisolone UNION ALL
	select 'rx_prednisone'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_prednisone UNION ALL
	select 'rx_rituximab'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_rituximab UNION ALL
	select 'rx_sirolimus'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_sirolimus UNION ALL
	select 'rx_tacrolimus'	 as variable, code, display, system, encounter_ref, medicationrequest_ref as resource_ref from irae__cohort_rx_tacrolimus
)
select distinct
    select_union.variable,
    select_union.code,
    select_union.display,
    select_union.system,
    select_union.resource_ref,
    sp.status,
    sp.age_at_visit,
    sp.age_group,
    sp.gender,
    sp.race_display,
    sp.ethnicity_display,
    sp.enc_period_ordinal,
    sp.enc_period_start_day,
    sp.enc_period_end_day,
    sp.enc_class_code,
    sp.enc_class_display,
    sp.enc_type_system,
    sp.enc_type_code,
    sp.enc_type_display,
    sp.enc_servicetype_system,
    sp.enc_servicetype_code,
    sp.enc_servicetype_display,
    sp.encounter_ref,
    sp.subject_ref
from
    select_union,
    irae__cohort_study_population as sp
where
    select_union.encounter_ref = sp.encounter_ref
;
