create or replace view kidney_transplant__study_period as select * from
(VALUES
    (date('$period_start'), date('$period_end'), $include_history)
) AS t (period_start, period_end, include_history);