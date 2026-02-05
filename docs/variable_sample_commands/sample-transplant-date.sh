#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Transplant Date
echo "Transplant Date"
docker compose run --rm -it\
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/Transplant-Date-notes.csv \
  --export-to ./samples/Transplant-Date-notes \
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-word "KDIGO" \
  --select-by-word "Recipient" \
  --select-by-word "Transplant" \
  --select-by-word "Donor" \
  --select-by-word "Donation" \
  --select-by-word "Organ" \
  --select-by-word "Transplant Date"  \
  --select-by-word "transplanted on" \
  --select-by-word "POD" \
  --select-by-word "transplant on"  \
  --select-by-regex "now day \+{0,1}\d+" \
  --select-by-regex "transplant \({0,1}\d+\s*\/\s*\d+\){0,1}" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"

