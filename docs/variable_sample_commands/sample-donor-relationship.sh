#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Donor Relationship
echo "Donor Relationship"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/donor-relationship.csv\
  --export-to ./samples/donor-relationship/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
    --select-by-word "KDIGO" \
  --select-by-word "Related Donor" \
  --select-by-word "Familial donor" \
  --select-by-word "Family donor" \
  --select-by-word "Sibling donor" \
  --select-by-word "Parent donor" \
  --select-by-word "Mother donor" \
  --select-by-word "Father donor" \
  --select-by-word "Child donor" \
  --select-by-word "Brother donor" \
  --select-by-word "Sister donor" \
  --select-by-word "Unrelated donor" \
  --select-by-word "directed donor" \
  --select-by-word "altruistic donor" \
  --select-by-word "good samaritan donor" \
  --select-by-word "anonymous donor" \
  --select-by-word "volunteer donor" \
  --select-by-word "NDD" \
  --select-by-word "non directed donor" \
  --select-by-word "non-directed donor" \
  --select-by-word "nondirected donor" \
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
