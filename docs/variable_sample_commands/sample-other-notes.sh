#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Other Notes
echo "Other Notes"
docker compose run --rm -it \
  cumulus-etl sample \
  $SAMPLE_INPUT_FOLDER \
  --output ./samples/other-notes.csv\
  --export-to ./samples/other-notes/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir $SAMPLE_PHI_DIR \
  --athena-database $SAMPLE_ATHENA_DB  \
  --athena-workgroup $SAMPLE_ATHENA_WORKGROUP \
  --athena-region $SAMPLE_ATHENA_REGION \
  --select-by-regex "^(?!.*(?:\bDeceased\ Renal\b|\bdirected\ donor\b|\bHLA\ Quality\b|\bCytomegalovirus\b|\bBrain\ dead\b|\bDonor\+\b|\bDonor\ neg\b|\bDeceased\ Donor\b|\bHeart\ beating\b|\bhigh\ mismatch\b|\bDonor\(\+\)\b|\bHLA\-DP\b|\bweak\ match\b|\bR\ \(\-\)\b|\bclose\ match\b|\bRelated\ Donor\b|\bantigen\ matches\b|\bcomplete\ match\b|\bgood\ samaritan\ donor\b|\bHLA\-C\b|\bLiving\ Donor\b|\bCMV\b|\bintermediate\ match\b|\bHLA\-A\b|\bRecip\-\b|\bDonor\(\-\)\b|\bfavorable\ match\b|\bBrain\-dead\b|\bSister\ donor\b|\bmismatched\b|\bseropositivity\b|\bTransplant\b|\bvolunteer\ donor\b|\bEpstein\-Barr\b|\bDonor\ \+\b|\bRecip\(\-\)\b|\bcadaver\b|\bLiving\ Renal\b|\bdonor\ serostatus\b|\bacceptable\ match\b|\bDesensitized\b|\bTransplant\ Date\b|\bRecip\(\+\)\b|\baltruistic\ donor\b|\bDD\ kidney\b|\bD\-pos\b|\bRecipient\ reactive\b|\btransplant\s*\(?\d+\s*/\s*\d+\)?\b|\bMother\ donor\b|\bRecip\ \(\+\)\b|\bunfavorably\ matched\b|\bHighly\ Sensitized\b|\bhuman\ leukocyte\ antigen\b|\bD\+\b|\bfull\ match\b|\bweakly\ matched\b|\bpoorly\ matched\b|\bUnrelated\ donor\b|\bexcellently\ matched\b|\bRecipient\b|\bDD\ donor\b|\bsuitable\ match\b|\bseronegativity\b|\bcompatible\ match\b|\bR\-\b|\bEBV\+\b|\bLive\ Donor\b|\bDonor\-negative\b|\bidentically\ matched\b|\bfavorably\ matched\b|\bR\ \-\b|\bNot\ Sensitized\b|\bDeceased\ Kidney\b|\bfully\ matched\b|\bD\ \(\-\)\b|\bRecip\ neg\b|\bD\ \+\b|\btransplant\ on\b|\bBrother\ donor\b|\bRecip\-negative\b|\bDD\ renal\b|\bnow day\s*\+?\d+\b|\bHLA\-DR\b|\bR\+\b|\bDDRT\b|\bcompletely\ matched\b|\bLive\ Kidney\b|\bPCR\b|\bFather\ donor\b|\bnon\ directed\ donor\b|\bperfect\ match\b|\bmismatches\b|\bCadaveric\b|\bEpstein\b|\bperfectly\ matched\b|\bHLA\-DQ\b|\bR\(\-\)\b|\bD\-\b|\bnon\-directed\ donor\b|\bCMV\+\b|\bR\(\+\)\b|\bR\-pos\b|\bRecip\ \+\b|\bhighly\ mismatched\b|\bRenal\ DD\b|\bfully\ matches\b|\bSensitization\b|\bgood\ match\b|\bDonor\ pos\b|\bseronegative\b|\bR\ \+\b|\bRecip\ pos\b|\bR\-neg\b|\bantigen\ matched\b|\bFamilial\ donor\b|\bDesensitization\b|\bKidney\ DD\b|\bliving\ relative\b|\bHLA\-B\b|\bpartial\ match\b|\btransplanted\ on\b|\bRecip\ \-\b|\bDonor\ \-\b|\bDonation\b|\bD\ \-\b|\bD\(\-\)\b|\bDonor\ nonreactive\b|\bDonor\-positive\b|\bCMV\-\b|\bD\(\+\)\b|\bRecipient\ nonreactive\b|\bLDRT\b|\bHLA\b|\bSensitized\b|\bSibling\ donor\b|\bIgG\ negative\b|\bliving\ related\ donor\b|\bacceptably\ matched\b|\bseropositive\b|\bLRD\b|\bDonor\-\b|\bRecip\-positive\b|\bAlloimmunized\b|\bLURD\b|\bexcellent\ match\b|\bpartially\ match\b|\bmoderate\ match\b|\bDonor\ \(\-\)\b|\bmoderately\ matched\b|\bPOD\b|\banonymous\ donor\b|\bwell\ matched\b|\bEBV\b|\bIgG\ positive\b|\bnondirected\ donor\b|\bpoor\ match\b|\bNDD\b|\bliving\ unrelated\ donor\b|\bKDIGO\b|\bParent\ donor\b|\bLive\ Renal\b|\bBeating\ heart\b|\bR\ \(\+\)\b|\bD\ \(\+\)\b|\bDeceased\ Organ\b|\bserostatus\b|\bFamily\ donor\b|\bDonor\ reactive\b|\bidentical\ match\b|\bDonor\ \(\+\)\b|\bmismatch\b|\bRecip\+\b|\bantigen\ match\b|\bDonor\b|\bclosely\ matched\b|\bRecip\ \(\-\)\b|\bChild\ donor\b|\brecipient\ serostatus\b|\bunfavorable\ match\b|\bD\-neg\b|\bLRRT\b|\bLiving\ Kidney\b))" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
