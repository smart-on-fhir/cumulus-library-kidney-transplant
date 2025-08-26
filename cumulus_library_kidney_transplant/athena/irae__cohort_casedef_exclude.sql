create TABLE irae__cohort_casedef_exclude as WITH
other_dx_transplant as (
    select  distinct
            valueset as exclude,
            system,
            code,
            display,
            subject_ref
    from    irae__cohort_dx_transplant
    where   CODE not in (select distinct CODE from irae__casedef)
    and     CODE != 'Z94.9' -- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/39
),
other_proc_transplant as (
    select  distinct
            valueset as exclude,
            system,
            code,
            display,
            subject_ref
    from    irae__cohort_proc_transplant
    where  CODE not in (select distinct CODE from irae__casedef)
),
index_date as (
    select  distinct
            'index_date' as exclude,
            idx.system,
            idx.code,
            idx.display,
            subject_ref
    from    irae__casedef as casedef,
            irae__cohort_casedef_index as idx
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
        irae__cohort_casedef.*
from    exclude_reasons,
        irae__cohort_casedef
where   exclude_reasons.subject_ref = irae__cohort_casedef.subject_ref
;