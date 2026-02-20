#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Any Rejection
echo "Any Rejection"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/any-rejection.csv\
  --export-to ./samples/any-rejection/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
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
  --select-by-word "Surveillance" \
  --select-by-word "Monitoring" \
  --select-by-word "Monitor" \
  --select-by-word "Vigilance" \
  --select-by-word "Vigilant" \
  --select-by-word "Watch" \
  --select-by-word "Watching" \
  --select-by-word "Screening" \
  --select-by-word "Screen" \
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
  --select-by-word "Biospecimen" \
  --select-by-word "Biosample" \
  --select-by-word "Specimen" \
  --select-by-word "Tissue" \
  --select-by-word "Resection" \
  --select-by-word "resected" \
  --select-by-word "re-excision" \
  --select-by-word "re-excised" \
  --select-by-word "re-excise" \
  --select-by-word "excise" \
  --select-by-word "excised" \
  --select-by-word "Graft" \
  --select-by-word "Allograft" \
  --select-by-word "Pathology" \
  --select-by-word "Pathological" \
  --select-by-word "IHC" \
  --select-by-word "immunohistochemistry" \
  --select-by-word "immunostain" \
  --select-by-word "immunostaining" \
  --select-by-word "histologic" \
  --select-by-word "staining" \
  --select-by-word "stain" \
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
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
