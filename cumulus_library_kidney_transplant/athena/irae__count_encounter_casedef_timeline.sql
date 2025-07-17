CREATE TABLE irae__count_encounter_casedef_timeline AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."enc_period_start_month",
            s."soe",
            s."valueset",
            s."variable"
            --noqa: enable=RF03, AL02
        FROM irae__cohort_casedef_timeline AS s
        WHERE s.status = 'finished'
    ),
    
    null_replacement AS (
        SELECT
            subject_ref,
            encounter_ref,
            coalesce(
                cast(enc_period_start_month AS varchar),
                'cumulus__none'
            ) AS enc_period_start_month,
            coalesce(
                cast(soe AS varchar),
                'cumulus__none'
            ) AS soe,
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
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "enc_period_start_month",
            "soe",
            "valueset",
            "variable",
            concat_ws(
                '-',
                COALESCE("enc_period_start_month",''),
                COALESCE("soe",''),
                COALESCE("valueset",''),
                COALESCE("variable",'')
            ) AS id
        FROM null_replacement
        WHERE encounter_ref IS NOT NULL
        GROUP BY
            cube(
            "enc_period_start_month",
            "soe",
            "valueset",
            "variable"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_period_start_month",
            "soe",
            "valueset",
            "variable",
            concat_ws(
                '-',
                COALESCE("enc_period_start_month",''),
                COALESCE("soe",''),
                COALESCE("valueset",''),
                COALESCE("variable",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_period_start_month",
            "soe",
            "valueset",
            "variable"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."enc_period_start_month",
        p."soe",
        p."valueset",
        p."variable"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        p.cnt_subject_ref >= 10
        AND s.cnt_encounter_ref >= 10
);