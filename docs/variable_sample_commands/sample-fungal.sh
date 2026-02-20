#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Fungal
echo "Fungal"
docker compose run --rm -it  cumulus-etl sample   <input folder with ndjson files from step 2 above>   --output ./samples/fungal.csv  --export-to ./samples/fungal/  --count 30   --seed 07201869   --columns "note,subject,encounter"   --phi-dir <your typical ETL PHI folder>   --athena-database <relevant_cumulus_library_database>    --athena-workgroup <relevant_cumulus_library_workgroup>   --athena-region <relevant_cumulus_region>   
  --select-by-athena-table irae__sample_casedef_peri   --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
