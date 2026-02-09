#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Donor Status
echo "Donor Status"
docker compose run --rm -it\
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/Donor-Status-notes.csv \
  --export-to ./samples/Donor-Status-notes \
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-word "KDIGO" \
  --select-by-word "Living Donor" \
  --select-by-word "Living Kidney" \
  --select-by-word "Living Renal" \
  --select-by-word "Live Donor" \
  --select-by-word "Live Renal" \
  --select-by-word "Live Kidney" \
  --select-by-word "LDRT" \
  --select-by-word "Deceased Donor" \
  --select-by-word "Deceased Kidney" \
  --select-by-word "Deceased Renal" \
  --select-by-word "Deceased Organ" \
  --select-by-word "Heart beating" \
  --select-by-word "Beating heart" \
  --select-by-word "Brain dead" \
  --select-by-word "Brain-dead" \
  --select-by-word "Cadaveric" \
  --select-by-word "cadaver" \
  --select-by-word "DD donor" \
  --select-by-word "DD kidney" \
  --select-by-word "DD renal" \
  --select-by-word "Renal DD" \
  --select-by-word "Kidney DD" \
  --select-by-word "DDRT" \
  --select-by-word "LRD" \
  --select-by-word "LRRT" \
  --select-by-word "living related donor" \
  --select-by-word "living relative" \
  --select-by-word "LURD" \
  --select-by-word "living unrelated donor" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"

