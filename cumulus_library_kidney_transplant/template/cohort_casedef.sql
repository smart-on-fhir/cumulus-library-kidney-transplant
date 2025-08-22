create table    irae__cohort_casedef as
select * from   irae__cohort_casedef_dx
UNION
select * from   irae__cohort_casedef_rx
UNION
select * from   irae__cohort_casedef_proc
UNION
select * from   irae__cohort_casedef_lab
UNION
select * from   irae__cohort_casedef_doc
UNION
select * from   irae__cohort_casedef_diag
;