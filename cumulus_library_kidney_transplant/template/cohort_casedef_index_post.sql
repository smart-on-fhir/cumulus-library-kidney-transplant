--    https://github.com/smart-on-fhir/cumulus-library-kidney-transplant/issues/87

create table irae__sample_casedef_index_post as
WITH index_post AS (
    SELECT 'index' AS casedef_period, *
    FROM irae__sample_casedef_index
    UNION ALL
    SELECT 'post' AS casedef_period, *
    FROM irae__sample_casedef_post
),
-- DISTINCT before PARTITION
index_post_uniq AS (
    SELECT DISTINCT
        subject_ref,
        documentreference_ref,
        sort_by_date
    FROM index_post
),
ordered AS (
    SELECT
        subject_ref,
        documentreference_ref,
        sort_by_date,
        ROW_NUMBER() OVER (
            PARTITION   BY  subject_ref
            ORDER       BY  sort_by_date,
                            documentreference_ref
        ) AS merged_doc_ordinal
    FROM index_post_uniq
)
SELECT      distinct
            index_post.*,
            ordered.merged_doc_ordinal
FROM        index_post,
            ordered
where       index_post.documentreference_ref = ordered.documentreference_ref
ORDER BY    subject_ref, merged_doc_ordinal, documentreference_ref;
