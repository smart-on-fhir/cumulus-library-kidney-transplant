create table irae__cohort_study_variables_lookup as
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_autoimmune' as variable from irae__cohort_dx_autoimmune
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_cancer' as variable from irae__cohort_dx_cancer
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_compromised' as variable from irae__cohort_dx_compromised
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_diabetes' as variable from irae__cohort_dx_diabetes
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_heart' as variable from irae__cohort_dx_heart
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_htn' as variable from irae__cohort_dx_htn
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_infection' as variable from irae__cohort_dx_infection
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_dx_kidney' as variable from irae__cohort_dx_kidney
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_rx_drug_levels' as variable from irae__cohort_rx_drug_levels
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_rx_htn' as variable from irae__cohort_rx_htn
UNION
select distinct subtype, code, display, system, encounter_ref, subject_ref, 'irae__cohort_rx_immunosuppressive' as variable from irae__cohort_rx_immunosuppressive







