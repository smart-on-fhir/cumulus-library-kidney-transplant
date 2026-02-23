#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Transplant Date
echo "Transplant Date"
docker compose run --rm -it \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output ./samples/transplant-date.csv\
  --export-to ./samples/transplant-date/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
  --select-by-word "KDIGO" \
  --select-by-word "Transplant Date" \
  --select-by-word "transplanted on" \
  --select-by-word "POD" \
  --select-by-word "transplant on" \
  --select-by-regex "now day\s*\+?\d+" \
  --select-by-regex "transplant\s*\(?\d+\s*/\s*\d+\)?" \
  --select-by-word "Recipient" \
  --select-by-word "Transplant" \
  --select-by-word "Donor" \
  --select-by-word "Donation" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
