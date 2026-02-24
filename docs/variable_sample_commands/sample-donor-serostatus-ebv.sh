#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"
echo 
echo "SAMPLE_INPUT_FOLDER: $SAMPLE_INPUT_FOLDER"
echo "SAMPLE_PHI_DIR: $SAMPLE_PHI_DIR"
echo "SAMPLE_ATHENA_DB: $SAMPLE_ATHENA_DB "
echo "SAMPLE_ATHENA_WORKGROUP: $SAMPLE_ATHENA_WORKGROUP"
echo "SAMPLE_ATHENA_REGION: $SAMPLE_ATHENA_REGION"


# Donor Serostatus EBV
echo "Donor Serostatus EBV"
docker compose run --rm -it \
  -v "$(pwd):/host" \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output /host/samples/donor-serostatus-ebv.csv\
  --export-to /host/samples/donor-serostatus-ebv/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
  --select-by-word "serostatus" \
  --select-by-word "seropositive" \
  --select-by-word "seropositivity" \
  --select-by-word "IgG positive" \
  --select-by-word "seronegative" \
  --select-by-word "seronegativity" \
  --select-by-word "IgG negative" \
  --select-by-word "Epstein-Barr" \
  --select-by-word "Epstein" \
  --select-by-word "EBV" \
  --select-by-word "EBV+" \
  --select-by-word "EBV-" \
  --select-by-word "donor serostatus" \
  --select-by-word "D-pos" \
  --select-by-word "Donor pos" \
  --select-by-word "Donor reactive" \
  --select-by-word "Donor-positive" \
  --select-by-word "D-neg" \
  --select-by-word "Donor neg" \
  --select-by-word "Donor nonreactive" \
  --select-by-word "Donor-negative" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
