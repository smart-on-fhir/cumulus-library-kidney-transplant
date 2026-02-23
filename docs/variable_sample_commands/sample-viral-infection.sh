#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Viral Infection
echo "Viral Infection"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/viral-infection.csv\
  --export-to ./samples/viral-infection/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-word "KDIGO" \
  --select-by-word "Epstein-Barr" \
  --select-by-word "Epstein" \
  --select-by-word "EBV" \
  --select-by-word "EBV+" \
  --select-by-word "Cytomegalovirus" \
  --select-by-word "CMV" \
  --select-by-word "CMV+" \
  --select-by-word "CMV-" \
  --select-by-word "Surveillance" \
  --select-by-word "Monitoring" \
  --select-by-word "Monitor" \
  --select-by-word "Vigilance" \
  --select-by-word "Vigilant" \
  --select-by-word "Watch" \
  --select-by-word "Watching" \
  --select-by-word "Screening" \
  --select-by-word "Screen" \
  --select-by-word "Prophylaxis" \
  --select-by-word "Prophylactic" \
  --select-by-word "Prevention" \
  --select-by-word "Preventive" \
  --select-by-word "Preemptive" \
  --select-by-word "Empiric" \
  --select-by-word "empirical" \
  --select-by-word "empirically" \
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
  --select-by-word "UTI" \
  --select-by-word "urinary tract infection" \
  --select-by-word "UTD" \
  --select-by-word "Hydronephrosis" \
  --select-by-word "VUR" \
  --select-by-word "Vesicoureteral Reflux" \
  --select-by-word "Ureter" \
  --select-by-word "Surgical site" \
  --select-by-word "SSI" \
  --select-by-word "Abscess" \
  --select-by-word "Wound" \
  --select-by-word "Catheter" \
  --select-by-word "CLABSI" \
  --select-by-word "Exit-site" \
  --select-by-word "Exit site" \
  --select-by-word "Purulence" \
  --select-by-word "Purulent" \
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
  --select-by-word "Antimicrobial" \
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
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
