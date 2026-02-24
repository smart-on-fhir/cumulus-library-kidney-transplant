#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"
echo 
echo "SAMPLE_INPUT_FOLDER: $SAMPLE_INPUT_FOLDER"
echo "SAMPLE_PHI_DIR: $SAMPLE_PHI_DIR"
echo "SAMPLE_ATHENA_DB: $SAMPLE_ATHENA_DB "
echo "SAMPLE_ATHENA_WORKGROUP: $SAMPLE_ATHENA_WORKGROUP"
echo "SAMPLE_ATHENA_REGION: $SAMPLE_ATHENA_REGION"


# Other Notes
echo "Other Notes"
docker compose run --rm -it \
  -v "$(pwd)/samples:/data/samples" \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output /data/samples/other-notes.csv\
  --export-to /data/samples/other-notes/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
  --select-by-regex "^(?!.*(?:\bAlloimmunized\b|\bBeating\ heart\b|\bBrain\ dead\b|\bBrain\-dead\b|\bBrother\ donor\b|\bCMV\b|\bCMV\+\b|\bCMV\-\b|\bCadaveric\b|\bChild\ donor\b|\bCytomegalovirus\b|\bDDRT\b|\bDD\ donor\b|\bDD\ kidney\b|\bDD\ renal\b|\bD\ \(\+\)\b|\bD\ \(\-\)\b|\bD\ \+\b|\bD\ \-\b|\bD\(\+\)\b|\bD\(\-\)\b|\bD\+\b|\bD\-\b|\bD\-neg\b|\bD\-pos\b|\bDeceased\ Donor\b|\bDeceased\ Kidney\b|\bDeceased\ Organ\b|\bDeceased\ Renal\b|\bDesensitization\b|\bDesensitized\b|\bDonation\b|\bDonor\b|\bDonor\ \(\+\)\b|\bDonor\ \(\-\)\b|\bDonor\ \+\b|\bDonor\ \-\b|\bDonor\ neg\b|\bDonor\ nonreactive\b|\bDonor\ pos\b|\bDonor\ reactive\b|\bDonor\(\+\)\b|\bDonor\(\-\)\b|\bDonor\+\b|\bDonor\-\b|\bDonor\-negative\b|\bDonor\-positive\b|\bEBV\b|\bEBV\+\b|\bEpstein\b|\bEpstein\-Barr\b|\bFamilial\ donor\b|\bFamily\ donor\b|\bFather\ donor\b|\bHLA\b|\bHLA\ Quality\b|\bHLA\-A\b|\bHLA\-B\b|\bHLA\-C\b|\bHLA\-DP\b|\bHLA\-DQ\b|\bHLA\-DR\b|\bHeart\ beating\b|\bHighly\ Sensitized\b|\bIgG\ negative\b|\bIgG\ positive\b|\bKDIGO\b|\bKidney\ DD\b|\bLDRT\b|\bLRD\b|\bLRRT\b|\bLURD\b|\bLive\ Donor\b|\bLive\ Kidney\b|\bLive\ Renal\b|\bLiving\ Donor\b|\bLiving\ Kidney\b|\bLiving\ Renal\b|\bMother\ donor\b|\bNDD\b|\bNot\ Sensitized\b|\bPCR\b|\bPOD\b|\bParent\ donor\b|\bR\ \(\+\)\b|\bR\ \(\-\)\b|\bR\ \+\b|\bR\ \-\b|\bR\(\+\)\b|\bR\(\-\)\b|\bR\+\b|\bR\-\b|\bR\-neg\b|\bR\-pos\b|\bRecip\ \(\+\)\b|\bRecip\ \(\-\)\b|\bRecip\ \+\b|\bRecip\ \-\b|\bRecip\ neg\b|\bRecip\ pos\b|\bRecip\(\+\)\b|\bRecip\(\-\)\b|\bRecip\+\b|\bRecip\-\b|\bRecip\-negative\b|\bRecip\-positive\b|\bRecipient\b|\bRecipient\ nonreactive\b|\bRecipient\ reactive\b|\bRelated\ Donor\b|\bRenal\ DD\b|\bSensitization\b|\bSensitized\b|\bSibling\ donor\b|\bSister\ donor\b|\bTransplant\b|\bTransplant\ Date\b|\bUnrelated\ donor\b|\bacceptable\ match\b|\bacceptably\ matched\b|\baltruistic\ donor\b|\banonymous\ donor\b|\bantigen\ match\b|\bantigen\ matched\b|\bantigen\ matches\b|\bcadaver\b|\bclose\ match\b|\bclosely\ matched\b|\bcompatible\ match\b|\bcomplete\ match\b|\bcompletely\ matched\b|\bdirected\ donor\b|\bdonor\ serostatus\b|\bexcellent\ match\b|\bexcellently\ matched\b|\bfavorable\ match\b|\bfavorably\ matched\b|\bfull\ match\b|\bfully\ matched\b|\bfully\ matches\b|\bgood\ match\b|\bgood\ samaritan\ donor\b|\bhigh\ mismatch\b|\bhighly\ mismatched\b|\bhuman\ leukocyte\ antigen\b|\bidentical\ match\b|\bidentically\ matched\b|\bintermediate\ match\b|\bliving\ related\ donor\b|\bliving\ relative\b|\bliving\ unrelated\ donor\b|\bmismatch\b|\bmismatched\b|\bmismatches\b|\bmoderate\ match\b|\bmoderately\ matched\b|\bnon\ directed\ donor\b|\bnon\-directed\ donor\b|\bnondirected\ donor\b|\bnow day\s*\+?\d+\b|\bpartial\ match\b|\bpartially\ match\b|\bperfect\ match\b|\bperfectly\ matched\b|\bpoor\ match\b|\bpoorly\ matched\b|\brecipient\ serostatus\b|\bseronegative\b|\bseronegativity\b|\bseropositive\b|\bseropositivity\b|\bserostatus\b|\bsuitable\ match\b|\btransplant\ on\b|\btransplant\s*\(?\d+\s*/\s*\d+\)?\b|\btransplanted\ on\b|\bunfavorable\ match\b|\bunfavorably\ matched\b|\bvolunteer\ donor\b|\bweak\ match\b|\bweakly\ matched\b|\bwell\ matched\b))" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
