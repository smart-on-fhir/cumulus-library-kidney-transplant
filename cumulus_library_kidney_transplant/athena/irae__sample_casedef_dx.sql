CREATE TABLE irae__sample_casedef_dx AS
SELECT  DISTINCT
        c.subject_ref, c.note_ordinal, c.days_since, c.note_ref, c.group_name
FROM    irae__sample_casedef                        as c
JOIN    irae__cohort_variable_union_dx    as v
        ON c.encounter_ref = v.encounter_ref
;

