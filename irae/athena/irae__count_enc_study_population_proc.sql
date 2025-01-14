CREATE TABLE irae__count_enc_study_population_proc AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."proc_display"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_population_proc AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(proc_display AS varchar),
                'cumulus__none'
            ) AS proc_display
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "proc_display",
            concat_ws(
                '-',
                COALESCE("proc_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "proc_display"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "proc_display",
            concat_ws(
                '-',
                COALESCE("proc_display",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "proc_display"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."proc_display"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);