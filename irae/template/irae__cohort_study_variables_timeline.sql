create table irae__cohort_study_variables_timeline as
select distinct
    dx_autoimmune,
    dx_cancer,
    dx_compromised,
    dx_diabetes,
    dx_heart,
    dx_htn,
    dx_infection,
    dx_kidney,
    rx_transplant,
    rx_immunosuppressive,
    SP.*
from
    irae__cohort_study_population as SP
left join irae__cohort_study_variables_table as V
    on SP.encounter_ref = V.encounter_ref;