#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Donor Serostatus EBV
echo "Donor Serostatus EBV"
docker compose run --rm -it\
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/Donor-Serostatus-EBV-notes.csv \
  --export-to ./samples/Donor-Serostatus-EBV-notes \
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
  --select-by-word "Organ" \
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
  --select-by-word "serostatus" \
  --select-by-word "seropositive" \
  --select-by-word "seropositivity" \
  --select-by-word "IgG positive" \
  --select-by-word "reactive" \
  --select-by-word "antibody detected" \
  --select-by-word "seronegative" \
  --select-by-word "seronegativity" \
  --select-by-word "IgG negative" \
  --select-by-word "non-reactive" \
  --select-by-word "no antibodies detected" \
  --select-by-word "serology" \
  --select-by-word "viral status" \
  --select-by-word "titer" \
  --select-by-word "screen" \
  --select-by-word "NAT" \
  --select-by-word "nucleic acid test" \
  --select-by-word "PCR" \
  --select-by-word "viral load" \
  --select-by-word "Ig markers" \
  --select-by-word "IgG" \
  --select-by-word "IgM" \
  --select-by-word "Total Ab" \
  --select-by-word "Antibody" \
  --select-by-word "Ab" \
  --select-by-word "Epstein-Barr" \
  --select-by-word "Epstein" \
  --select-by-word "EBV" \
  --select-by-word "EBV+" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection


# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"

