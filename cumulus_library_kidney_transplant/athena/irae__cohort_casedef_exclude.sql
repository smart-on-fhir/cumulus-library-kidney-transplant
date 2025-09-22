create TABLE irae__cohort_casedef_exclude as WITH
TransplantDx as (
    select  distinct
            valueset, system, code, display,
            subject_ref
    from    irae__cohort_dx_transplant
    where   CODE not in (select distinct CODE from irae__casedef)
    and     CODE not in ('Z94.9', 'V42.9') -- https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/39
),
TransplantProc as (
    select  distinct
            valueset, system, code, display,
            subject_ref
    from    irae__cohort_proc_transplant
    where  CODE not in (select distinct CODE from irae__casedef)
),
IndexDate as
(
    select  min(enc_period_start_day) as index_date,
            subject_ref
    from    irae__cohort_casedef
    where   include
    group by subject_ref
),
Complication as
(
    select  min(enc_period_start_day) as index_date,
            subject_ref, valueset, code, display, system
    from    irae__cohort_casedef
    where   NOT include
    group by subject_ref, valueset, code, display, system
),
IndexDateComplication as
(
    select  distinct
            valueset, system, code, display,
            Complication.subject_ref
    from    IndexDate, Complication
    where   IndexDate.subject_ref = Complication.subject_ref
    and     IndexDate.index_date > Complication.index_date
),
ExcludeReasons as (
    select * from TransplantDx
    UNION ALL
    select * from TransplantProc
    UNION ALL
    select * from IndexDateComplication
)
select  distinct
        ExcludeReasons.*
from    ExcludeReasons,
        irae__cohort_casedef as CaseDef
where   ExcludeReasons.subject_ref = CaseDef.subject_ref
;