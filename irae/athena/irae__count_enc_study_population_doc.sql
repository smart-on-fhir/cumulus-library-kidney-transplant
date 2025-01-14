CREATE TABLE irae__count_enc_study_population_doc AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."doc_type_display"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_doc AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(doc_type_display AS varchar),
                'cumulus__none'
            ) AS doc_type_display
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "doc_type_display",
            concat_ws(
                '-',
                COALESCE("doc_type_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "doc_type_display"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "doc_type_display",
            concat_ws(
                '-',
                COALESCE("doc_type_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "doc_type_display"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."doc_type_display"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);