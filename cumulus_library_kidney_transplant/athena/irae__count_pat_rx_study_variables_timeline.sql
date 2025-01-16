CREATE TABLE irae__count_pat_rx_study_variables_timeline AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."enc_period_start_year",
            s."lab_autoimmune",
            s."lab_creatinine",
            s."lab_custom",
            s."lab_diabetes",
            s."lab_gfr",
            s."lab_lft"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_study_variables_timeline AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(enc_period_start_year AS varchar),
                'cumulus__none'
            ) AS enc_period_start_year,
            coalesce(
                cast(lab_autoimmune AS varchar),
                'cumulus__none'
            ) AS lab_autoimmune,
            coalesce(
                cast(lab_creatinine AS varchar),
                'cumulus__none'
            ) AS lab_creatinine,
            coalesce(
                cast(lab_custom AS varchar),
                'cumulus__none'
            ) AS lab_custom,
            coalesce(
                cast(lab_diabetes AS varchar),
                'cumulus__none'
            ) AS lab_diabetes,
            coalesce(
                cast(lab_gfr AS varchar),
                'cumulus__none'
            ) AS lab_gfr,
            coalesce(
                cast(lab_lft AS varchar),
                'cumulus__none'
            ) AS lab_lft
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "enc_period_start_year",
            "lab_autoimmune",
            "lab_creatinine",
            "lab_custom",
            "lab_diabetes",
            "lab_gfr",
            "lab_lft",
            concat_ws(
                '-',
                COALESCE("enc_period_start_year",''),
                COALESCE("lab_autoimmune",''),
                COALESCE("lab_creatinine",''),
                COALESCE("lab_custom",''),
                COALESCE("lab_diabetes",''),
                COALESCE("lab_gfr",''),
                COALESCE("lab_lft",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_period_start_year",
            "lab_autoimmune",
            "lab_creatinine",
            "lab_custom",
            "lab_diabetes",
            "lab_gfr",
            "lab_lft"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_period_start_year",
            "lab_autoimmune",
            "lab_creatinine",
            "lab_custom",
            "lab_diabetes",
            "lab_gfr",
            "lab_lft",
            concat_ws(
                '-',
                COALESCE("enc_period_start_year",''),
                COALESCE("lab_autoimmune",''),
                COALESCE("lab_creatinine",''),
                COALESCE("lab_custom",''),
                COALESCE("lab_diabetes",''),
                COALESCE("lab_gfr",''),
                COALESCE("lab_lft",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_period_start_year",
            "lab_autoimmune",
            "lab_creatinine",
            "lab_custom",
            "lab_diabetes",
            "lab_gfr",
            "lab_lft"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."enc_period_start_year",
        p."lab_autoimmune",
        p."lab_creatinine",
        p."lab_custom",
        p."lab_diabetes",
        p."lab_gfr",
        p."lab_lft"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);