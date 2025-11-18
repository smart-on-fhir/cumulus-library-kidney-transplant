create table $prefix__cohort_study_variables_wide as
with lookup as
(
    select  distinct variable, valueset, encounter_ref
    from    $prefix__cohort_study_variables
),
join_study_period as
(
    select  distinct
            $variable_list_lookup,
            SP.encounter_ref
    from    $prefix__cohort_study_period as SP
    left join lookup on SP.encounter_ref = lookup.encounter_ref
),
tabular as
(
    select  distinct
            $variable_list_wide,
            encounter_ref
    from    join_study_period
    group by encounter_ref
)
select  distinct
        status              	,
        age_at_visit        	,
        gender              	,
        race_display        	,
        ethnicity_display   	,
        enc_period_ordinal  	,
        enc_period_start_day	,
        enc_period_start_week	,
        enc_period_start_month	,
        enc_period_start_year	,
        enc_period_end_day  	,
        enc_class_code      	,
        enc_servicetype_code	,
        enc_servicetype_system	,
        enc_servicetype_display	,
        enc_type_code       	,
        enc_type_system     	,
        enc_type_display    	,
        study_pop.encounter_ref ,
        study_pop.subject_ref
from    irae__cohort_study_population as study_pop,
        tabular
where   tabular.encounter_ref = study_pop.encounter_ref




