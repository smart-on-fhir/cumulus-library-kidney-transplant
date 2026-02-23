#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Death
echo "Death"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/death.csv\
  --export-to ./samples/death/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-word "Cadaveric" \
  --select-by-word "cadaver" \
  --select-by-word "Sepsis" \
  --select-by-word "Sepsis-like" \
  --select-by-word "Septic" \
  --select-by-word "Septicemia" \
  --select-by-word "Shock" \
  --select-by-word "SIRS" \
  --select-by-word "Death" \
  --select-by-word "dead" \
  --select-by-word "died" \
  --select-by-word "passed away" \
  --select-by-word "end of life" \
  --select-by-word "did not survive" \
  --select-by-word "passed peacefully" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
