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
  --select-by-regex "^(?!.*(?:\bliving\ related\ donor\b|\bexcellent\ match\b|\bwell\ matched\b|\bD\-neg\b|\bPCR\b|\bsuitable\ match\b|\bD\ \-\b|\bCMV\+\b|\bCMV\-\b|\bpartial\ match\b|\bKDIGO\b|\bLRRT\b|\bD\ \+\b|\bD\ \(\+\)\b|\btransplant\s*\(?\d+\s*/\s*\d+\)?\b|\bRecip\+\b|\bR\ \-\b|\bidentical\ match\b|\bDeceased\ Donor\b|\bD\ \(\-\)\b|\btransplanted\ on\b|\bcompatible\ match\b|\bLiving\ Donor\b|\bRecipient\ nonreactive\b|\bTransplant\ Date\b|\bIgG\ negative\b|\bweak\ match\b|\bParent\ donor\b|\btransplant\ on\b|\bfully\ matches\b|\bDonor\ \(\-\)\b|\bpartially\ match\b|\bD\+\b|\bCadaveric\b|\bMother\ donor\b|\bHLA\-C\b|\bR\ \+\b|\bLive\ Renal\b|\bLive\ Donor\b|\bLiving\ Kidney\b|\bLURD\b|\bD\-pos\b|\bDonor\+\b|\bmoderate\ match\b|\bNot\ Sensitized\b|\bSensitized\b|\bfull\ match\b|\bEBV\+\b|\bLive\ Kidney\b|\bEpstein\-Barr\b|\brecipient\ serostatus\b|\bRecip\ neg\b|\bBrain\-dead\b|\bHLA\-DQ\b|\bBrain\ dead\b|\bRenal\ DD\b|\bunfavorable\ match\b|\bDonor\ \-\b|\bDonor\ nonreactive\b|\bUnrelated\ donor\b|\bHLA\-A\b|\bDeceased\ Kidney\b|\bantigen\ matches\b|\bHLA\-DR\b|\bseropositive\b|\bgood\ samaritan\ donor\b|\bseronegativity\b|\bHeart\ beating\b|\bDonor\ \(\+\)\b|\bfully\ matched\b|\bmismatched\b|\bNDD\b|\bfavorably\ matched\b|\bhighly\ mismatched\b|\bFather\ donor\b|\bperfect\ match\b|\bD\-\b|\bPOD\b|\bclose\ match\b|\bclosely\ matched\b|\bR\-\b|\bRecip\-negative\b|\bRecip\(\+\)\b|\bRecipient\b|\bRelated\ Donor\b|\bDonor\(\-\)\b|\bmoderately\ matched\b|\bRecip\ pos\b|\bDonor\b|\bHLA\ Quality\b|\bnondirected\ donor\b|\bintermediate\ match\b|\baltruistic\ donor\b|\bDonor\ \+\b|\bpoor\ match\b|\bhuman\ leukocyte\ antigen\b|\bDesensitization\b|\bRecip\ \(\+\)\b|\bBeating\ heart\b|\bidentically\ matched\b|\bperfectly\ matched\b|\bhigh\ mismatch\b|\bR\(\-\)\b|\bD\(\-\)\b|\bSibling\ donor\b|\bSensitization\b|\bR\-pos\b|\bvolunteer\ donor\b|\bliving\ relative\b|\bRecip\ \+\b|\bDeceased\ Organ\b|\bDonor\(\+\)\b|\bR\-neg\b|\bLiving\ Renal\b|\bAlloimmunized\b|\bseropositivity\b|\bEpstein\b|\bRecipient\ reactive\b|\bliving\ unrelated\ donor\b|\bCytomegalovirus\b|\bpoorly\ matched\b|\bChild\ donor\b|\bLRD\b|\bHLA\-B\b|\bgood\ match\b|\bRecip\ \(\-\)\b|\bOrgan\b|\bFamily\ donor\b|\bunfavorably\ matched\b|\bserostatus\b|\bfavorable\ match\b|\bcomplete\ match\b|\bDonation\b|\bDD\ kidney\b|\bantigen\ match\b|\bR\(\+\)\b|\bcompletely\ matched\b|\bnow day\s*\+?\d+\b|\bDonor\-positive\b|\bLDRT\b|\bnon\ directed\ donor\b|\bDonor\ pos\b|\bmismatches\b|\bDonor\-\b|\bnon\-directed\ donor\b|\bHLA\-DP\b|\bKidney\ DD\b|\bHLA\b|\bantigen\ matched\b|\bHighly\ Sensitized\b|\bdonor\ serostatus\b|\bR\ \(\+\)\b|\bRecip\-\b|\bacceptable\ match\b|\bD\(\+\)\b|\bcadaver\b|\bmismatch\b|\bexcellently\ matched\b|\bacceptably\ matched\b|\bR\+\b|\bSister\ donor\b|\bDonor\ reactive\b|\bEBV\b|\bdirected\ donor\b|\bIgG\ positive\b|\bTransplant\b|\bDD\ donor\b|\bBrother\ donor\b|\bDeceased\ Renal\b|\bweakly\ matched\b|\bDonor\ neg\b|\banonymous\ donor\b|\bCMV\b|\bR\ \(\-\)\b|\bDesensitized\b|\bRecip\(\-\)\b|\bseronegative\b|\bDDRT\b|\bFamilial\ donor\b|\bDonor\-negative\b|\bDD\ renal\b|\bRecip\ \-\b|\bRecip\-positive\b))" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"
