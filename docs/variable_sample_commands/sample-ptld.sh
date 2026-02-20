#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# PTLD
echo "PTLD"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/ptld.csv\
  --export-to ./samples/ptld/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
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
  --select-by-word "Infection" \
  --select-by-word "Infections" \
  --select-by-word "Infectious" \
  --select-by-word "Infected" \
  --select-by-word "Infect" \
  --select-by-word "Opportunistic" \
  --select-by-word "Invasion" \
  --select-by-word "Invades" \
  --select-by-word "Invaded" \
  --select-by-word "Invade" \
  --select-by-word "Pathogenic" \
  --select-by-word "Pathogen" \
  --select-by-word "Antigen" \
  --select-by-word "Virulent" \
  --select-by-word "Virulence" \
  --select-by-word "Microorganism" \
  --select-by-word "Sepsis" \
  --select-by-word "Sepsis-like" \
  --select-by-word "Septic" \
  --select-by-word "Septicemia" \
  --select-by-word "Shock" \
  --select-by-word "SIRS" \
  --select-by-word "PNA" \
  --select-by-word "Pneumonia" \
  --select-by-word "Pneumoniae" \
  --select-by-word "Viral" \
  --select-by-word "Virus" \
  --select-by-word "Viremia" \
  --select-by-word "BK Virus" \
  --select-by-word "BK Viral" \
  --select-by-word "BKV" \
  --select-by-word "BKV+" \
  --select-by-word "BKN" \
  --select-by-word "Polyomaviridae" \
  --select-by-word "SV40" \
  --select-by-word "Herpes" \
  --select-by-word "HSV" \
  --select-by-word "HSV+" \
  --select-by-word "Zoster" \
  --select-by-word "VZV" \
  --select-by-word "VZV+" \
  --select-by-word "Shingles" \
  --select-by-word "Varicella" \
  --select-by-word "Hepatitis" \
  --select-by-word "HBV" \
  --select-by-word "HBV+" \
  --select-by-word "HCV" \
  --select-by-word "HCV+" \
  --select-by-word "Microbe" \
  --select-by-word "Microbial" \
  --select-by-word "Polymicrobial" \
  --select-by-word "Colonization" \
  --select-by-word "Colonized" \
  --select-by-word "Colonies" \
  --select-by-word "Colony" \
  --select-by-word "Antimicrobial" \
  --select-by-word "PTLD" \
  --select-by-word "Lymphoproliferative" \
  --select-by-word "Lymphoproliferation" \
  --select-by-word "Proliferative" \
  --select-by-word "Proliferating" \
  --select-by-word "Proliferate" \
  --select-by-word "Proliferated" \
  --select-by-word "Cancers" \
  --select-by-word "Cancer" \
  --select-by-word "Proliferation" \
  --select-by-word "Proliferative" \
  --select-by-word "Proliferate" \
  --select-by-word "Metastatic" \
  --select-by-word "Malignant" \
  --select-by-word "Malignancy" \
  --select-by-word "Hyperplasia" \
  --select-by-word "Hyperplastic" \
  --select-by-word "Neoplasia" \
  --select-by-word "Neoplastic" \
  --select-by-word "Neoplasm" \
  --select-by-word "Biopsy" \
  --select-by-word "Biopsies" \
  --select-by-word "Biospecimen" \
  --select-by-word "Biosample" \
  --select-by-word "Specimen" \
  --select-by-word "Tissue" \
  --select-by-word "Pathology" \
  --select-by-word "Pathological" \
  --select-by-word "IHC" \
  --select-by-word "immunohistochemistry" \
  --select-by-word "immunostain" \
  --select-by-word "immunostaining" \
  --select-by-word "histologic" \
  --select-by-word "staining" \
  --select-by-word "stain" \
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
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
