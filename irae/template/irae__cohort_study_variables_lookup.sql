create table irae__cohort_study_variables_lookup as
select distinct 'dx_autoimmune'     as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_autoimmune     UNION
select distinct 'dx_cancer'         as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_cancer         UNION
select distinct 'dx_compromised'    as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_compromised    UNION
select distinct 'dx_diabetes'       as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_diabetes       UNION
select distinct 'dx_heart'          as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_heart          UNION
select distinct 'dx_htn'            as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_htn            UNION
select distinct 'dx_infection'      as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_infection      UNION
select distinct 'dx_kidney'         as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_dx_kidney         UNION
select distinct 'rx_custom'         as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_rx_custom         UNION
select distinct 'rx_diabetes'       as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_rx_diabetes       UNION
select distinct 'rx_diuretics'      as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_rx_diuretics      UNION
select distinct 'rx_htn'            as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_rx_htn            UNION
select distinct 'rx_immunosuppressive' as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_rx_immunosuppressive UNION
select distinct 'lab_autoimmune'    as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_lab_autoimmune    UNION
select distinct 'lab_custom'        as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_lab_custom        UNION
select distinct 'lab_creatinine'    as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_lab_creatinine    UNION
select distinct 'lab_diabetes'      as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_lab_diabetes      UNION
select distinct 'lab_gfr'           as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_lab_gfr           UNION
select distinct 'lab_lft'           as variable, subtype, code, display, system, encounter_ref, subject_ref from irae__cohort_lab_lft
