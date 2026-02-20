#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Failure
echo "Failure"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/failure.csv\
  --export-to ./samples/failure/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-word "Cadaveric" \
  --select-by-word "cadaver" \
  --select-by-word "Inflammation" \
  --select-by-word "Inflammatory" \
  --select-by-word "Inflamed" \
  --select-by-word "Glomerulonephritis" \
  --select-by-word "Pyelonephritis" \
  --select-by-word "Nephritis" \
  --select-by-word "Tubulitis" \
  --select-by-word "Enteritis" \
  --select-by-word "Ureteritis" \
  --select-by-word "Cellulitis" \
  --select-by-word "Peritonitis" \
  --select-by-word "Endocarditis" \
  --select-by-word "Erythema" \
  --select-by-word "Edema" \
  --select-by-word "Sepsis" \
  --select-by-word "Sepsis-like" \
  --select-by-word "Septic" \
  --select-by-word "Septicemia" \
  --select-by-word "Shock" \
  --select-by-word "SIRS" \
  --select-by-word "Dysfunction" \
  --select-by-word "Disfunction" \
  --select-by-word "nonfunctional" \
  --select-by-word "non functional" \
  --select-by-word "nonfunctioning" \
  --select-by-word "not functioning" \
  --select-by-word "Graft Function" \
  --select-by-word "Allograft Function" \
  --select-by-word "Kidney Function" \
  --select-by-word "Renal Function" \
  --select-by-word "Biopsy" \
  --select-by-word "Biopsies" \
  --select-by-word "Graft" \
  --select-by-word "Allograft" \
  --select-by-word "Rejection" \
  --select-by-word "Rejected" \
  --select-by-word "Reject" \
  --select-by-word "AMR" \
  --select-by-word "Antibody-Mediated" \
  --select-by-word "Antibody Mediated" \
  --select-by-word "DSA" \
  --select-by-word "DSAs" \
  --select-by-word "Donor specific" \
  --select-by-word "Antibodies" \
  --select-by-word "Antibody" \
  --select-by-word "B-cells" \
  --select-by-word "B cells" \
  --select-by-word "B lymphocytes" \
  --select-by-word "B-lymphocytes" \
  --select-by-word "B-cell" \
  --select-by-word "B cell" \
  --select-by-word "B lymphocyte" \
  --select-by-word "B-lymphocyte" \
  --select-by-word "T-cells" \
  --select-by-word "T cells" \
  --select-by-word "T lymphocytes" \
  --select-by-word "T-lymphocytes" \
  --select-by-word "T-cell" \
  --select-by-word "T cell" \
  --select-by-word "T lymphocyte" \
  --select-by-word "T-lymphocyte" \
  --select-by-word "TCMR" \
  --select-by-word "ACR" \
  --select-by-word "Cytotoxic" \
  --select-by-word "Acute cellular" \
  --select-by-word "Banff" \
  --select-by-word "Grading" \
  --select-by-word "Grade" \
  --select-by-word "Failure" \
  --select-by-word "Failed" \
  --select-by-word "Fail" \
  --select-by-word "Fibrosis" \
  --select-by-word "Fibrotic" \
  --select-by-word "Stenosis" \
  --select-by-word "Ischemia" \
  --select-by-word "Narrowing" \
  --select-by-word "Stricture" \
  --select-by-word "Obstruction" \
  --select-by-word "Thrombosis" \
  --select-by-word "Thrombotic" \
  --select-by-word "Microangiopathy" \
  --select-by-word "Renal vein" \
  --select-by-word "Renal artery" \
  --select-by-word "Dialysis" \
  --select-by-word "Hemodialysis" \
  --select-by-word "Peritoneal" \
  --select-by-word "Nephrectomy" \
  --select-by-word "Graftectomy" \
  --select-by-word "Explantation" \
  --select-by-word "Removal" \
  --select-by-word "Removed" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
