CREATE TABLE irae__count_pat_dx_study_variables_timeline AS (
    WITH
    filtered_table AS (
        SELECT
            s.subject_ref,
            s.encounter_ref,
            --noqa: disable=RF03, AL02
            s."enc_period_start_year",
            s."variable",
            s."dx_autoimmune",
            s."dx_cancer",
            s."dx_compromised",
            s."dx_diabetes",
            s."dx_heart",
            s."dx_htn",
            s."dx_infection",
            s."dx_kidney"
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
                cast(variable AS varchar),
                'cumulus__none'
            ) AS variable,
            coalesce(
                cast(dx_autoimmune AS varchar),
                'cumulus__none'
            ) AS dx_autoimmune,
            coalesce(
                cast(dx_cancer AS varchar),
                'cumulus__none'
            ) AS dx_cancer,
            coalesce(
                cast(dx_compromised AS varchar),
                'cumulus__none'
            ) AS dx_compromised,
            coalesce(
                cast(dx_diabetes AS varchar),
                'cumulus__none'
            ) AS dx_diabetes,
            coalesce(
                cast(dx_heart AS varchar),
                'cumulus__none'
            ) AS dx_heart,
            coalesce(
                cast(dx_htn AS varchar),
                'cumulus__none'
            ) AS dx_htn,
            coalesce(
                cast(dx_infection AS varchar),
                'cumulus__none'
            ) AS dx_infection,
            coalesce(
                cast(dx_kidney AS varchar),
                'cumulus__none'
            ) AS dx_kidney
        FROM filtered_table
    ),
    secondary_powerset AS (
        SELECT
            count(DISTINCT encounter_ref) AS cnt_encounter_ref,
            "enc_period_start_year",
            "variable",
            "dx_autoimmune",
            "dx_cancer",
            "dx_compromised",
            "dx_diabetes",
            "dx_heart",
            "dx_htn",
            "dx_infection",
            "dx_kidney",
            concat_ws(
                '-',
                COALESCE("enc_period_start_year",''),
                COALESCE("variable",''),
                COALESCE("dx_autoimmune",''),
                COALESCE("dx_cancer",''),
                COALESCE("dx_compromised",''),
                COALESCE("dx_diabetes",''),
                COALESCE("dx_heart",''),
                COALESCE("dx_htn",''),
                COALESCE("dx_infection",''),
                COALESCE("dx_kidney",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_period_start_year",
            "variable",
            "dx_autoimmune",
            "dx_cancer",
            "dx_compromised",
            "dx_diabetes",
            "dx_heart",
            "dx_htn",
            "dx_infection",
            "dx_kidney"
            )
    ),

    powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject_ref,
            "enc_period_start_year",
            "variable",
            "dx_autoimmune",
            "dx_cancer",
            "dx_compromised",
            "dx_diabetes",
            "dx_heart",
            "dx_htn",
            "dx_infection",
            "dx_kidney",
            concat_ws(
                '-',
                COALESCE("enc_period_start_year",''),
                COALESCE("variable",''),
                COALESCE("dx_autoimmune",''),
                COALESCE("dx_cancer",''),
                COALESCE("dx_compromised",''),
                COALESCE("dx_diabetes",''),
                COALESCE("dx_heart",''),
                COALESCE("dx_htn",''),
                COALESCE("dx_infection",''),
                COALESCE("dx_kidney",'')
            ) AS id
        FROM null_replacement
        GROUP BY
            cube(
            "enc_period_start_year",
            "variable",
            "dx_autoimmune",
            "dx_cancer",
            "dx_compromised",
            "dx_diabetes",
            "dx_heart",
            "dx_htn",
            "dx_infection",
            "dx_kidney"
            )
    )

    SELECT
        s.cnt_encounter_ref AS cnt,
        p."enc_period_start_year",
        p."variable",
        p."dx_autoimmune",
        p."dx_cancer",
        p."dx_compromised",
        p."dx_diabetes",
        p."dx_heart",
        p."dx_htn",
        p."dx_infection",
        p."dx_kidney"
    FROM powerset AS p
    JOIN secondary_powerset AS s on s.id = p.id
    WHERE 
        cnt_subject_ref >= 10
);