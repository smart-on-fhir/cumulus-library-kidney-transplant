--     enc_class_code
--     enc_class_display,
--     enc_start_date,
--     enc_end_date,
--     gender,
--     race_display,
--     age_at_visit,
--     doc_date,
--     doc_author_date,
--     doc_type_display,
--     doc_type_code,

create or replace view irae__gpt4_donor_vars as
select  distinct
        encounter_ref,
        documentreference_ref,
        subject_ref,
        gender,
        race_display,
        age_at_visit,
        enc_start_date,
        doc_date,
        donor_date_mentioned,
        doc_type_display,
        donor_type,
        donor_type_mentioned,
        donor_date,
        donor_relationship,
        donor_relationship_mentioned,
        donor_hla_quality,
        donor_hla_mismatch
from irae__gpt4_fhir;

create or replace view irae__gpt4_donor_date as
WITH date_counts AS (
    SELECT
        subject_ref,
        donor_date,
        COUNT(*) AS cnt
    from    irae__gpt4_donor_vars
    where   donor_date is not null
    and     donor_date > date('2000-01-01')
    GROUP BY subject_ref, donor_date
),
ranked_dates AS (
    SELECT  cnt, subject_ref, donor_date,
        ROW_NUMBER() OVER (
            PARTITION BY subject_ref
            ORDER BY cnt DESC, donor_date ASC  -- break ties consistently
        ) AS rn
    FROM date_counts
)
SELECT      cnt, subject_ref,
            donor_date as donor_date_min
FROM        ranked_dates
WHERE       rn = 1
ORDER BY    subject_ref;


create or replace view irae__gpt4_donor as
       select   var.*,
                idx.donor_date_min,
                date_trunc('month', idx.donor_date_min) as donor_date_min_month,
                date_trunc('year', idx.donor_date_min) as donor_date_min_year
       from     irae__gpt4_donor_vars   as  var,
                irae__gpt4_donor_date   as  idx
       where    var.subject_ref = idx.subject_ref;

-- create or replace irae__gpt4_donor as
--        select   irae__gpt4_donor_vars.*,
--                 idx.donor_date,
--                 date_trunc('month', idx.donor_date) as donor_date_month
--        from     irae__gpt4_donor_vars   as  var,
--                 irae__gpt4_donor_date   as  idx
--        where    var.subject_ref = idx.subject_ref;