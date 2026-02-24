#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"
echo 
echo "SAMPLE_INPUT_FOLDER: $SAMPLE_INPUT_FOLDER"
echo "SAMPLE_PHI_DIR: $SAMPLE_PHI_DIR"
echo "SAMPLE_ATHENA_DB: $SAMPLE_ATHENA_DB "
echo "SAMPLE_ATHENA_WORKGROUP: $SAMPLE_ATHENA_WORKGROUP"
echo "SAMPLE_ATHENA_REGION: $SAMPLE_ATHENA_REGION"


# Donor Relationship
echo "Donor Relationship"
docker compose run --rm -it \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output ./samples/donor-relationship.csv\
  --export-to ./samples/donor-relationship/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
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
