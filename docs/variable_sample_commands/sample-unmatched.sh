#!/bin/bash

start_time=$(date +%s)
echo "Process started at: $(date)"

# Other Notes - sample from any note except for keyword matches
echo "Other Notes - sample from any note except for keyword matches"
docker compose run --rm -it\
  cumulus-etl sample \
  <input folder with ndjson files from step 2 above> \
  --output ./samples/Other-notes.csv \
  --export-to ./samples/Other-notes \
  --count 30 \
  --seed 07201869 \
  --columns "note,subject,encounter" \
  --phi-dir <your typical ETL PHI folder> \
  --athena-database <relevant_cumulus_library_database>  \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --athena-region <relevant_cumulus_region> \
  --select-by-regex "^(?!.*(?:\bKDIGO\b|\bRelated\ Donor\b|\bFamilial\ donor\b|\bFamily\ donor\b|\bSibling\ donor\b|\bParent\ donor\b|\bMother\ donor\b|\bFather\ donor\b|\bChild\ donor\b|\bBrother\ donor\b|\bSister\ donor\b|\bUnrelated\ donor\b|\bdirected\ donor\b|\baltruistic\ donor\b|\bgood\ samaritan\ donor\b|\banonymous\ donor\b|\bvolunteer\ donor\b|\bNDD\b|\bnon\ directed\ donor\b|\bnon\-directed\ donor\b|\bnondirected\ donor\b|\bLRD\b|\bLRRT\b|\bliving\ related\ donor\b|\bliving\ relative\b|\bLURD\b|\bliving\ unrelated\ donor\b|\bRecipient\b|\bTransplant\b|\bDonor\b|\bDonation\b|\bOrgan\b|\bdonor\ serostatus\b|\bD\+\b|\bD\ \+\b|\bD\(\+\)\b|\bD\ \(\+\)\b|\bD\-pos\b|\bDonor\ pos\b|\bDonor\+\b|\bDonor\ \+\b|\bDonor\(\+\)\b|\bDonor\ \(\+\)\b|\bDonor\ reactive\b|\bDonor\-positive\b|\bD\-\b|\bD\ \-\b|\bD\(\-\)\b|\bD\ \(\-\)\b|\bD\-neg\b|\bDonor\ neg\b|\bDonor\-\b|\bDonor\ \-\b|\bDonor\(\-\)\b|\bDonor\ \(\-\)\b|\bDonor\ nonreactive\b|\bDonor\-negative\b|\bserostatus\b|\bseropositive\b|\bseropositivity\b|\bIgG\ positive\b|\breactive\b|\bantibody\ detected\b|\bseronegative\b|\bseronegativity\b|\bIgG\ negative\b|\bnon\-reactive\b|\bno\ antibodies\ detected\b|\bserology\b|\bviral\ status\b|\btiter\b|\bscreen\b|\bNAT\b|\bnucleic\ acid\ test\b|\bPCR\b|\bviral\ load\b|\bIg\ markers\b|\bIgG\b|\bIgM\b|\bTotal\ Ab\b|\bAntibody\b|\bAb\b|\bCytomegalovirus\b|\bCMV\b|\bCMV\+\b|\bCMV\-\b|\bEpstein\-Barr\b|\bEpstein\b|\bEBV\b|\bEBV\+\b|\bLiving\ Donor\b|\bLiving\ Kidney\b|\bLiving\ Renal\b|\bLive\ Donor\b|\bLive\ Renal\b|\bLive\ Kidney\b|\bLDRT\b|\bDeceased\ Donor\b|\bDeceased\ Kidney\b|\bDeceased\ Renal\b|\bDeceased\ Organ\b|\bHeart\ beating\b|\bBeating\ heart\b|\bBrain\ dead\b|\bBrain\-dead\b|\bCadaveric\b|\bcadaver\b|\bDD\ donor\b|\bDD\ kidney\b|\bDD\ renal\b|\bRenal\ DD\b|\bKidney\ DD\b|\bHLA\b|\bhuman\ leukocyte\ antigen\b|\bantigen\ matched\b|\bantigen\ matches\b|\bantigen\ match\b|\bmismatch\b|\bmismatches\b|\bmismatched\b|\bwell\ matched\b|\bgood\ match\b|\bexcellent\ match\b|\bexcellently\ matched\b|\bfavorable\ match\b|\bfavorably\ matched\b|\bclose\ match\b|\bclosely\ matched\b|\bfully\ matched\b|\bfully\ matches\b|\bfull\ match\b|\bcomplete\ match\b|\bcompletely\ matched\b|\bperfect\ match\b|\bperfectly\ matched\b|\bidentical\ match\b|\bidentically\ matched\b|\bmoderately\ matched\b|\bmoderate\ match\b|\bpartial\ match\b|\bpartially\ match\b|\bintermediate\ match\b|\bacceptable\ match\b|\bacceptably\ matched\b|\bsuitable\ match\b|\bcompatible\ match\b|\bpoorly\ matched\b|\bpoor\ match\b|\bweak\ match\b|\bweakly\ matched\b|\bhigh\ mismatch\b|\bhighly\ mismatched\b|\bunfavorable\ match\b|\bunfavorably\ matched\b|\bDSA\b|\bDSAs\b|\bDonor\ specific\b|\bHLA\ Quality\b|\bHighly\ Sensitized\b|\bAlloimmunized\b|\bDesensitization\b|\bDesensitized\b|\brecipient\ serostatus\b|\bR\+\b|\bR\ \+\b|\bR\(\+\)\b|\bR\ \(\+\)\b|\bR\-pos\b|\bRecip\ pos\b|\bRecip\+\b|\bRecip\ \+\b|\bRecip\(\+\)\b|\bRecip\ \(\+\)\b|\bRecipient\ reactive\b|\bRecip\-positive\b|\bR\-\b|\bR\ \-\b|\bR\(\-\)\b|\bR\ \(\-\)\b|\bR\-neg\b|\bRecip\ neg\b|\bRecip\-\b|\bRecip\ \-\b|\bRecip\(\-\)\b|\bRecip\ \(\-\)\b|\bRecipient\ nonreactive\b|\bRecip\-negative\b|\bTransplant\ Date\b|\btransplanted\ on\b|\bPOD\b|\btransplant\ on\b|\bnow day\s*\+?\d+\b|\btransplant\s*\(?\d+\s*/\s*\d+\)?\b|\bOperationOutcome\b))" \
  --select-by-athena-table irae__sample_casedef_peri \
  --allow-large-selection

# Record end time
end_time=$(date +%s)
elapsed=$((end_time - start_time))

echo "Process finished at: $(date)"
echo "Total duration: $elapsed seconds"

