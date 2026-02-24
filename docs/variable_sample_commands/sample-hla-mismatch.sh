#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"
echo 
echo "SAMPLE_INPUT_FOLDER: $SAMPLE_INPUT_FOLDER"
echo "SAMPLE_PHI_DIR: $SAMPLE_PHI_DIR"
echo "SAMPLE_ATHENA_DB: $SAMPLE_ATHENA_DB "
echo "SAMPLE_ATHENA_WORKGROUP: $SAMPLE_ATHENA_WORKGROUP"
echo "SAMPLE_ATHENA_REGION: $SAMPLE_ATHENA_REGION"


# HLA Mismatch
echo "HLA Mismatch"
docker compose run --rm -it \
  -v "$(pwd):/host" \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output /host/samples/hla-mismatch.csv\
  --export-to /host/samples/hla-mismatch/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
  --select-by-word "KDIGO" \
  --select-by-word "HLA" \
  --select-by-word "human leukocyte antigen" \
  --select-by-word "antigen matched" \
  --select-by-word "antigen matches" \
  --select-by-word "antigen match" \
  --select-by-word "HLA-A" \
  --select-by-word "HLA-B" \
  --select-by-word "HLA-C" \
  --select-by-word "HLA-DR" \
  --select-by-word "HLA-DQ" \
  --select-by-word "HLA-DP" \
  --select-by-word "mismatch" \
  --select-by-word "mismatches" \
  --select-by-word "mismatched" \
  --select-by-word "well matched" \
  --select-by-word "good match" \
  --select-by-word "excellent match" \
  --select-by-word "excellently matched" \
  --select-by-word "favorable match" \
  --select-by-word "favorably matched" \
  --select-by-word "close match" \
  --select-by-word "closely matched" \
  --select-by-word "fully matched" \
  --select-by-word "fully matches" \
  --select-by-word "full match" \
  --select-by-word "complete match" \
  --select-by-word "completely matched" \
  --select-by-word "perfect match" \
  --select-by-word "perfectly matched" \
  --select-by-word "identical match" \
  --select-by-word "identically matched" \
  --select-by-word "moderately matched" \
  --select-by-word "moderate match" \
  --select-by-word "partial match" \
  --select-by-word "partially match" \
  --select-by-word "intermediate match" \
  --select-by-word "acceptable match" \
  --select-by-word "acceptably matched" \
  --select-by-word "suitable match" \
  --select-by-word "compatible match" \
  --select-by-word "poorly matched" \
  --select-by-word "poor match" \
  --select-by-word "weak match" \
  --select-by-word "weakly matched" \
  --select-by-word "high mismatch" \
  --select-by-word "highly mismatched" \
  --select-by-word "unfavorable match" \
  --select-by-word "unfavorably matched" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
