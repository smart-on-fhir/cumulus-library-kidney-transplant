#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Fungal Infection
echo "Fungal Infection"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/fungal-infection.csv\
  --export-to ./samples/fungal-infection/\
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
  --select-by-word "Antimicrobial" \
  --select-by-word "Mycobacterium" \
  --select-by-word "Mycobacteria" \
  --select-by-word "Fungal" \
  --select-by-word "Fungemia" \
  --select-by-word "Fungus" \
  --select-by-word "Mold" \
  --select-by-word "Yeast" \
  --select-by-word "Mycosis" \
  --select-by-word "Mycotic" \
  --select-by-word "Pneumocystis" \
  --select-by-word "Pneumocystosis" \
  --select-by-word "Jirovecii" \
  --select-by-word "PCP" \
  --select-by-word "PJP" \
  --select-by-word "Candida" \
  --select-by-word "Candidiasis" \
  --select-by-word "Aspergillus" \
  --select-by-word "Aspergillosis" \
  --select-by-word "Fumigatus" \
  --select-by-word "Mycosis" \
  --select-by-word "Mycotic" \
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
