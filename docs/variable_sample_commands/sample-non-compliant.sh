#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Non Compliant
echo "Non Compliant"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/non-compliant.csv\
  --export-to ./samples/non-compliant/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
    --select-by-word "therapeutic" \
  --select-by-word "within range" \
  --select-by-word "at goal" \
  --select-by-word "at target" \
  --select-by-word "goal level" \
  --select-by-word "target level" \
  --select-by-word "target range" \
  --select-by-word "appropriate level" \
  --select-by-word "adequate level" \
  --select-by-word "acceptable level" \
  --select-by-word "stable level" \
  --select-by-word "good level" \
  --select-by-word "subtherapeutic" \
  --select-by-word "inadequate level" \
  --select-by-word "insufficient level" \
  --select-by-word "below goal" \
  --select-by-word "below level" \
  --select-by-word "below range" \
  --select-by-word "below target" \
  --select-by-word "under goal" \
  --select-by-word "under level" \
  --select-by-word "under range" \
  --select-by-word "under target" \
  --select-by-word "not at goal" \
  --select-by-word "not at target" \
  --select-by-word "supratherapeutic" \
  --select-by-word "bolus" \
  --select-by-word "supra level" \
  --select-by-word "elevated level" \
  --select-by-word "excessive level" \
  --select-by-word "above level" \
  --select-by-word "above goal" \
  --select-by-word "above range" \
  --select-by-word "above target" \
  --select-by-word "over target" \
  --select-by-word "high level" \
  --select-by-word "toxic level" \
  --select-by-word "above range" \
  --select-by-word "above therapeutic" \
  --select-by-word "above target" \
  --select-by-word "Trough" \
  --select-by-word "Level" \
  --select-by-word "Levels" \
  --select-by-word "Target" \
  --select-by-word "Goal" \
  --select-by-word "Baseline" \
  --select-by-word "Immunosuppression" \
  --select-by-word "immunosuppressive" \
  --select-by-word "immunosuppressant" \
  --select-by-word "Compliant" \
  --select-by-word "Compliance" \
  --select-by-word "taking as prescribed" \
  --select-by-word "taking medications" \
  --select-by-word "taking regularly" \
  --select-by-word "takes medications" \
  --select-by-word "takes meds" \
  --select-by-word "regularly taking" \
  --select-by-word "regularly takes" \
  --select-by-word "Partially Compliant" \
  --select-by-word "partial compliance" \
  --select-by-word "partially adherent" \
  --select-by-word "sometimes compliant" \
  --select-by-word "partial adherence" \
  --select-by-word "intermittently compliant" \
  --select-by-word "sometimes compliant" \
  --select-by-word "inconsistent adherence" \
  --select-by-word "inconsistent with meds" \
  --select-by-word "occasionally misses doses" \
  --select-by-word "occasional missed doses" \
  --select-by-word "takes meds irregularly" \
  --select-by-word "incomplete compliance" \
  --select-by-word "Noncompliant" \
  --select-by-word "non-compliant" \
  --select-by-word "not compliant" \
  --select-by-word "non adherence" \
  --select-by-word "non-adherent" \
  --select-by-word "not adherent" \
  --select-by-word "poor compliance" \
  --select-by-word "poor adherence" \
  --select-by-word "fails to take meds" \
  --select-by-word "fails to take medications" \
  --select-by-word "does not take meds" \
  --select-by-word "does not take medications" \
  --select-by-word "stopped taking meds" \
  --select-by-word "refuses medication" \
  --select-by-word "missed doses" \
  --select-by-word "frequently misses doses" \
  --select-by-word "frequent missed doses" \
  --select-by-word "Adherence" \
  --select-by-word "Adheres" \
  --select-by-word "Adhere" \
  --select-by-word "Surveillance" \
  --select-by-word "Monitoring" \
  --select-by-word "Monitor" \
  --select-by-word "Vigilance" \
  --select-by-word "Vigilant" \
  --select-by-word "Watch" \
  --select-by-word "Watching" \
  --select-by-word "Screening" \
  --select-by-word "Screen" \
  --select-by-word "Tracking" \
  --select-by-word "Track" \
  --select-by-word "Oversight" \
  --select-by-word "Oversee" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
