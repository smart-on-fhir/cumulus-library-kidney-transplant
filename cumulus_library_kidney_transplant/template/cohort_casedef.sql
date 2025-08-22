create table    $prefix__cohort_casedef as
select * from   $prefix__cohort_casedef_dx
UNION
select * from   $prefix__cohort_casedef_rx
UNION
select * from   $prefix__cohort_casedef_proc
UNION
select * from   $prefix__cohort_casedef_lab
UNION
select * from   $prefix__cohort_casedef_doc
UNION
select * from   $prefix__cohort_casedef_diag
;