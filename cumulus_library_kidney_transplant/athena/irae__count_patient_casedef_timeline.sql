CREATE TABLE irae__count_patient_casedef_timeline AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            --noqa: disable=RF03, AL02
            s."enc_period_start_month",
            s."period",
            s."valueset",
            s."variable"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_casedef_timeline AS s
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            coalesce(
                cast(enc_period_start_month AS varchar),
                'cumulus__none'
            ) AS enc_period_start_month,
            coalesce(
                cast(period AS varchar),
                'cumulus__none'
            ) AS period,
            coalesce(
                cast(valueset AS varchar),
                'cumulus__none'
            ) AS valueset,
            coalesce(
                cast(variable AS varchar),
                'cumulus__none'
            ) AS variable
        FROM filtered_table
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_period_start_month",
            "period",
            "valueset",
            "variable",
            concat_ws(
                '-',
                COALESCE("enc_period_start_month",''),
                COALESCE("period",''),
                COALESCE("valueset",''),
                COALESCE("variable",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_period_start_month",
            "period",
            "valueset",
            "variable"
            )
    )

    SELECT
        p.cnt_subject_ref AS cnt,
        p."enc_period_start_month",
        p."period",
        p."valueset",
        p."variable"
    FROM powerset AS p
    WHERE 
        p.cnt_subject_ref >= 10
);