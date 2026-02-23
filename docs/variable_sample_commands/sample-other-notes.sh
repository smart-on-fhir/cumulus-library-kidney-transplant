#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Other Notes
echo "Other Notes"
docker compose run --rm -it \
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/other-notes.csv\
  --export-to ./samples/other-notes/\
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-regex "^(?!.*(?:\bLiving\ Donor\b|\bFamilial\ donor\b|\bRenal\ DD\b|\bpoorly\ matched\b|\bR\ \+\b|\bDeceased\ Kidney\b|\bHLA\-A\b|\bRecip\ \+\b|\bRecip\ \-\b|\bacceptably\ matched\b|\btransplant\s*\(?\d+\s*/\s*\d+\)?\b|\bRecip\ pos\b|\bLiving\ Renal\b|\bD\ \+\b|\baltruistic\ donor\b|\bHLA\-DR\b|\bRecip\ neg\b|\bCMV\-\b|\bCytomegalovirus\b|\bMother\ donor\b|\bcompletely\ matched\b|\bEpstein\b|\bKidney\ DD\b|\bcompatible\ match\b|\bLive\ Donor\b|\bnon\-directed\ donor\b|\bDesensitized\b|\bEBV\b|\bR\(\+\)\b|\bcomplete\ match\b|\brecipient\ serostatus\b|\bIgG\ negative\b|\bDesensitization\b|\bdonor\ serostatus\b|\bmismatch\b|\bLURD\b|\bR\ \-\b|\bHLA\-B\b|\bHLA\-DP\b|\bDonor\ neg\b|\bD\ \(\-\)\b|\bDonor\-negative\b|\bSensitization\b|\bpoor\ match\b|\bfully\ matches\b|\bD\(\-\)\b|\bLDRT\b|\bwell\ matched\b|\bBrain\ dead\b|\bgood\ samaritan\ donor\b|\bweakly\ matched\b|\bAlloimmunized\b|\bserostatus\b|\bgood\ match\b|\bdirected\ donor\b|\bfully\ matched\b|\bhigh\ mismatch\b|\bBrain\-dead\b|\bD\-pos\b|\bD\-\b|\bDonor\-\b|\bChild\ donor\b|\bPOD\b|\bTransplant\b|\bR\ \(\+\)\b|\bclose\ match\b|\bsuitable\ match\b|\bUnrelated\ donor\b|\bmismatched\b|\bperfectly\ matched\b|\bDonor\ \(\-\)\b|\bD\+\b|\banonymous\ donor\b|\bidentically\ matched\b|\bNot\ Sensitized\b|\bCMV\b|\bRecip\+\b|\bRecip\-\b|\bKDIGO\b|\bpartially\ match\b|\bD\ \(\+\)\b|\bDDRT\b|\bclosely\ matched\b|\bParent\ donor\b|\bBrother\ donor\b|\bRecipient\ reactive\b|\bliving\ relative\b|\btransplanted\ on\b|\bnon\ directed\ donor\b|\bDonor\b|\bhighly\ mismatched\b|\bRecip\(\+\)\b|\bLive\ Kidney\b|\bRecip\ \(\+\)\b|\bEpstein\-Barr\b|\bHLA\b|\bDonor\ \-\b|\bseronegative\b|\bD\-neg\b|\bRecip\ \(\-\)\b|\bFather\ donor\b|\bNDD\b|\bfavorably\ matched\b|\bcadaver\b|\bfull\ match\b|\bDonor\ pos\b|\bIgG\ positive\b|\bLiving\ Kidney\b|\bDonor\(\+\)\b|\bantigen\ matches\b|\bmoderate\ match\b|\bHLA\ Quality\b|\bEBV\+\b|\bvolunteer\ donor\b|\bDonor\ \(\+\)\b|\bDD\ kidney\b|\bexcellent\ match\b|\bunfavorable\ match\b|\bDonor\-positive\b|\bHLA\-C\b|\bRecip\-positive\b|\bliving\ unrelated\ donor\b|\bnondirected\ donor\b|\bmoderately\ matched\b|\bDeceased\ Donor\b|\bR\(\-\)\b|\bLRD\b|\bRecip\-negative\b|\bDD\ donor\b|\bDD\ renal\b|\bTransplant\ Date\b|\bintermediate\ match\b|\bDonor\ nonreactive\b|\bHighly\ Sensitized\b|\bDonor\ reactive\b|\bDonation\b|\bFamily\ donor\b|\bR\-neg\b|\bseropositive\b|\bhuman\ leukocyte\ antigen\b|\bRecipient\b|\bpartial\ match\b|\bperfect\ match\b|\bRecip\(\-\)\b|\bunfavorably\ matched\b|\bDeceased\ Organ\b|\bliving\ related\ donor\b|\bseronegativity\b|\bDonor\(\-\)\b|\bseropositivity\b|\bD\ \-\b|\bnow day\s*\+?\d+\b|\bLive\ Renal\b|\bexcellently\ matched\b|\bacceptable\ match\b|\bSensitized\b|\bHLA\-DQ\b|\bPCR\b|\bCMV\+\b|\bRecipient\ nonreactive\b|\bCadaveric\b|\bR\-\b|\bDonor\ \+\b|\bHeart\ beating\b|\bidentical\ match\b|\bRelated\ Donor\b|\bR\+\b|\bantigen\ match\b|\bSibling\ donor\b|\bweak\ match\b|\bR\-pos\b|\bSister\ donor\b|\bantigen\ matched\b|\bfavorable\ match\b|\bR\ \(\-\)\b|\btransplant\ on\b|\bLRRT\b|\bBeating\ heart\b|\bD\(\+\)\b|\bDonor\+\b|\bmismatches\b|\bDeceased\ Renal\b))" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
