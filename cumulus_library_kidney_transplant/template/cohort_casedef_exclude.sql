create TABLE $prefix__cohort_casedef_exclude as WITH
other_dx_transplant as (
    select  distinct
            valueset as exclude,
            system,
            code,
            display,
            subject_ref
    from    $prefix__cohort_dx_transplant
    where   CODE not in (select distinct CODE from $prefix__casedef)
    and     CODE != 'Z94.9' -- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/39
),
other_proc_transplant as (
    select  distinct
            valueset as exclude,
            system,
            code,
            display,
            subject_ref
    from    $prefix__cohort_proc_transplant
    where  CODE not in (select distinct CODE from $prefix__casedef)
),
index_date as (
    select  distinct
            'index_date' as exclude,
            idx.system,
            idx.code,
            idx.display,
            subject_ref
    from    $prefix__casedef as casedef,
            $prefix__cohort_casedef_index as idx
    where   NOT casedef.include
    and     casedef.system  = idx.system
    and     casedef.code    = idx.code
),
exclude_reasons as (
    select * from other_dx_transplant
    UNION ALL
    select * from other_proc_transplant
    UNION ALL
    select * from index_date
)
select  distinct
        exclude_reasons.exclude,
        $prefix__cohort_casedef.*
from    exclude_reasons,
        $prefix__cohort_casedef
where   exclude_reasons.subject_ref = $prefix__cohort_casedef.subject_ref
;