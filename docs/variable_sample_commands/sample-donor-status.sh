#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"
echo 
echo "SAMPLE_INPUT_FOLDER: $SAMPLE_INPUT_FOLDER"
echo "SAMPLE_PHI_DIR: $SAMPLE_PHI_DIR"
echo "SAMPLE_ATHENA_DB: $SAMPLE_ATHENA_DB "
echo "SAMPLE_ATHENA_WORKGROUP: $SAMPLE_ATHENA_WORKGROUP"
echo "SAMPLE_ATHENA_REGION: $SAMPLE_ATHENA_REGION"


# Donor Status
echo "Donor Status"
docker compose run --rm -it \
  -v "$(pwd)/samples:/data/samples" \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output /data/samples/donor-status.csv\
  --export-to /data/samples/donor-status/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
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
