create table irae__cohort_study_variables_pair as
select distinct
    SV1.variable as variable1,
    SV1.valueset as valueset1,
    SV2.variable as variable2,
    SV2.valueset as valueset2,
    SV1.status,
    SV1.gender,
    SV1.race_display as race_display1,
    SV2.race_display as race_display2,
    SV1.age_at_visit as age_at_visit1,
    SV2.age_at_visit as age_at_visit2,
    SV1.encounter_ref as encounter_ref1,
    SV2.encounter_ref as encounter_ref2,
    SV1.enc_period_start_day    as enc_period_start_day1,
    SV2.enc_period_start_day    as enc_period_start_day2,
    SV1.subject_ref
from irae__cohort_study_variables as SV1,
     irae__cohort_study_variables as SV2
where
    SV1.subject_ref = SV2.subject_ref
and SV1.enc_period_start_day <= SV2.enc_period_start_day
