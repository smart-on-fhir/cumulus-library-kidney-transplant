#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"
echo 
echo "SAMPLE_INPUT_FOLDER: $SAMPLE_INPUT_FOLDER"
echo "SAMPLE_PHI_DIR: $SAMPLE_PHI_DIR"
echo "SAMPLE_ATHENA_DB: $SAMPLE_ATHENA_DB "
echo "SAMPLE_ATHENA_WORKGROUP: $SAMPLE_ATHENA_WORKGROUP"
echo "SAMPLE_ATHENA_REGION: $SAMPLE_ATHENA_REGION"


# Recipient Serostatus EBV
echo "Recipient Serostatus EBV"
docker compose run --rm -it \
  -v "$(pwd):/host" \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output /host/samples/recipient-serostatus-ebv.csv\
  --export-to /host/samples/recipient-serostatus-ebv/\
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
  --select-by-word "PCR" \
  --select-by-word "Epstein-Barr" \
  --select-by-word "Epstein" \
  --select-by-word "EBV" \
  --select-by-word "EBV+" \
  --select-by-word "recipient serostatus" \
  --select-by-word "R+" \
  --select-by-word "R +" \
  --select-by-word "R(+)" \
  --select-by-word "R (+)" \
  --select-by-word "R-pos" \
  --select-by-word "Recip pos" \
  --select-by-word "Recip+" \
  --select-by-word "Recip +" \
  --select-by-word "Recip(+)" \
  --select-by-word "Recip (+)" \
  --select-by-word "Recipient reactive" \
  --select-by-word "Recip-positive" \
  --select-by-word "R-" \
  --select-by-word "R -" \
  --select-by-word "R(-)" \
  --select-by-word "R (-)" \
  --select-by-word "R-neg" \
  --select-by-word "Recip neg" \
  --select-by-word "Recip-" \
  --select-by-word "Recip -" \
  --select-by-word "Recip(-)" \
  --select-by-word "Recip (-)" \
  --select-by-word "Recipient nonreactive" \
  --select-by-word "Recip-negative" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
