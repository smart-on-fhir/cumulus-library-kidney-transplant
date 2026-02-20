#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# HLA Quality
echo "HLA Quality"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/hla-quality.csv\
  --export-to ./samples/hla-quality/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
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
  --select-by-word "HLA Quality" \
  --select-by-word "Highly Sensitized" \
  --select-by-word "Not Sensitized" \
  --select-by-word "Alloimmunized" \
  --select-by-word "Desensitization" \
  --select-by-word "Desensitized" \
  --select-by-word "Sensitized" \
  --select-by-word "Sensitization" \
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
