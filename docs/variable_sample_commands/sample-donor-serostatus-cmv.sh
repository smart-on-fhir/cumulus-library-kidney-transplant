#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Donor Serostatus CMV
echo "Donor Serostatus CMV"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/donor-serostatus-cmv.csv\
  --export-to ./samples/donor-serostatus-cmv/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-word "Recipient" \
  --select-by-word "Transplant" \
  --select-by-word "Donor" \
  --select-by-word "Donation" \
  --select-by-word "serostatus" \
  --select-by-word "seropositive" \
  --select-by-word "seropositivity" \
  --select-by-word "IgG positive" \
  --select-by-word "seronegative" \
  --select-by-word "seronegativity" \
  --select-by-word "IgG negative" \
  --select-by-word "PCR" \
  --select-by-word "Cytomegalovirus" \
  --select-by-word "CMV" \
  --select-by-word "CMV+" \
  --select-by-word "CMV-" \
  --select-by-word "donor serostatus" \
  --select-by-word "D+" \
  --select-by-word "D +" \
  --select-by-word "D(+)" \
  --select-by-word "D (+)" \
  --select-by-word "D-pos" \
  --select-by-word "Donor pos" \
  --select-by-word "Donor+" \
  --select-by-word "Donor +" \
  --select-by-word "Donor(+)" \
  --select-by-word "Donor (+)" \
  --select-by-word "Donor reactive" \
  --select-by-word "Donor-positive" \
  --select-by-word "D-" \
  --select-by-word "D -" \
  --select-by-word "D(-)" \
  --select-by-word "D (-)" \
  --select-by-word "D-neg" \
  --select-by-word "Donor neg" \
  --select-by-word "Donor-" \
  --select-by-word "Donor -" \
  --select-by-word "Donor(-)" \
  --select-by-word "Donor (-)" \
  --select-by-word "Donor nonreactive" \
  --select-by-word "Donor-negative" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
