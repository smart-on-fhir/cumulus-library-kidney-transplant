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
    SV1.enc_class_code as enc_class_code1,
    SV2.enc_class_code as enc_class_code2,
    SV1.subject_ref
from irae__cohort_study_variables as SV1,
     irae__cohort_study_variables as SV2
where
    SV1.subject_ref = SV2.subject_ref;
