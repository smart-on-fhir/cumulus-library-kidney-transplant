#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Subtherapeutic 
echo "Subtherapeutic "
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/subtherapeutic-.csv\
  --export-to ./samples/subtherapeutic-/\
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
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
