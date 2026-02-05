# Running the IRAE Kidney Transplant study

This guide will help you reproduce the kidney study from scratch. At a high level, the
kidney study and related NLP breaks down into five steps: 
1. Building the initial Kidney-Study tables
2. Running NLP detecting immunosuppressive medication against peri-operative notes (from casedef_index)
3. Running NLP detecting history of multiple transplants against peri-operative notes (from casedef_index)
4. Running NLP detecting donor characteristics against peri-operative notes (from casedef_index)
5. Running NLP detecting outcome variables against post-transplant notes (from casedef_post)

In addition to running NLP against notes, each NLP task above also entails:
- Populating a relevant highlights table in athena based on those annotations; and
- Uploading notes for chart-review, pre-labelled based on LLM annotations.

Note that these instructions only use the `irae__sample_casedef_*_10` sample of 10 patients 
created by the kidney study. Full runs of this work should reference the full set of notes, at 
`irae__sample_casedef_*`.

A reminder that PHI-free example notes and example LLM responses can be found in our [cumulus-kidney-transplant-examples](https://github.com/smart-on-fhir/cumulus-kidney-transplant-examples) repo. Specifically, LLM responses for our four tasks can be found under [/examples/fhir/llm-output](https://github.com/smart-on-fhir/cumulus-kidney-transplant-examples/tree/main/examples/fhir/llm-output)

## Prerequisites

- An existing Cumulus stack, with an already-built `core` study.
  - See the general [Cumulus documentation](https://docs.smarthealthit.org/cumulus/)
    for setting that up.
- Familiarity with [creating new cumulus library studies](https://docs.smarthealthit.org/cumulus/library/creating-studies.html#creating-library-studies)
- Familiarity with [running NLP workflows using cumulus etl](https://docs.smarthealthit.org/cumulus/etl/nlp/example.html)
- This module should be installed in the same python environment as the cumulus stack. This can 
  be done by running `pip install cumulus-library-kidney-transplant`, which will add an `irae` target 
  to `cumulus-library`. 
- **Lastly, make sure that your cloud environment has been updated to use the [latest set of DeltaTables](https://github.com/smart-on-fhir/cumulus-etl/blob/main/docs/setup/cumulus-aws-template.yaml). To support these numerous new tasks, new tables have been introduced.**

## 1. Run the ETL & Library study

First we want to build our cohort of interest with this kidney 
study and [cumulus-library](https://docs.smarthealthit.org/cumulus/library/) 
like so: 
```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae 
```

You should now have all the interesting results sitting in Athena, with the exception of 
`irae__highlights_*` tables. We will build these after running NLP, but that requires first 
building our study and defining our patient cohort.

## 2. Preparing our DocumentReferences 

Our various NLP tasks will examine two sets of document references: 
1. Peri-operative Notes (defined by `irae__sample_casedef_index_10`)
2. Post-transplant Notes (defined by `irae__sample_casedef_post_10`) 

You can save off the information your data unarchive process will need from these 
tables. Sanity checking the number of patients, notes, and encounters we have across kidney 
study sample tables, run the following: 
```sql
-- We should see 10 patients in our case definition
-- You can also do the same for casedef_post
select 
       count(distinct subject_ref)   as cnt_pat, 
       count(distinct encounter_ref) as cnt_enc,
       count(distinct documentreference_ref) as cnt_doc
from irae__sample_casedef_index_10
```


## 3. Prepare Your Data

This study operates on DocumentReference resources
(it runs NLP on the referenced clinical notes).
So we need to gather the original documents 

Gather some DocumentReference ndjson from your EHR.
You can either re-export the documents of interest,
or use ndjson from a previous export. Ideally these notes
are pre-inlined with clinical note content, as this will 
save time/hassle re-downloading the notes every time we run 
NLP. If you're gathering notes using our `smart-fetch` tool 
the notes should be [inlined automatically when exporting](https://docs.smarthealthit.org/cumulus/fetch/hydration.html#inlining-clinical-notes).

Place the ndjson in a folder, and take note of the paths to 
both your peri-operative notes and your post-operative notes
for later steps.


## 4. Run NLP 

Using the `cumulus-etl` tool, we will now run our IRAE specific NLP tasks. These instructions  
are for an [on-prem](https://docs.smarthealthit.org/cumulus/etl/nlp/example.html#local-on-prem-options) `gpt-oss-120b` instance, 
but support for other cloud-based models is available in the [example-nlp setup docs](https://docs.smarthealthit.org/cumulus/etl/nlp/example.html#model-setup).
Note that using other models will require updating the `gpt-oss-120b` specific arguments below. 

First you want to set up the GPT-OSS instance to run locally:
```sh
docker compose up --wait gpt-oss-120b
```

Once the LLM instance is up and running via docker, you can run the various `cumulus-etl nlp` tasks.

### 4.a. Immunosuppressive Medications against peri-operative notes
```sh
docker compose run --rm -it\
  cumulus-etl nlp \
  --task irae__nlp_immunosuppressive_medications_gpt_oss_120b \
  <input folder with peri-operative ndjson files from step 3 above> \
  <your typical ETL PHI folder> \
  <your typical ETL OUTPUT folder> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae__sample_casedef_index_10
```

### 4.b. History of Multiple Transplants against peri-operative notes
```sh
docker compose run --rm -it\
  cumulus-etl nlp \
  --task irae__nlp_multiple_transplant_history_gpt_oss_120b \
  <input folder with peri-operative ndjson files from step 3 above> \
  <your typical ETL PHI folder> \
  <your typical ETL OUTPUT folder> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae__sample_casedef_index_10
```

### 4.c. Donor Characteristics against peri-operative notes
```sh
docker compose run --rm -it\
  cumulus-etl nlp \
  --task irae__nlp_donor_gpt_oss_120b \
  <input folder with peri-operative ndjson files from step 3 above> \
  <your typical ETL PHI folder> \
  <your typical ETL OUTPUT folder> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae__sample_casedef_index_10
```

### 4.d. Outcome Variables against post-operative notes
```sh
docker compose run --rm -it\
  cumulus-etl nlp \
  --task irae__nlp_gpt_oss_120b \
  <input folder with **post-operative** ndjson files from step 3 above> \
  <your typical ETL PHI folder> \
  <your typical ETL OUTPUT folder> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table **irae__sample_casedef_post_10**
```

Note: by running with `-it` we can trigger an interactive run of docker compose, which 
allows us to take advantage of the `cumulus-etl nlp`'s support for verifying the number of notes 
that will be processed with NLP before starting a run. This can be useful in ensuring that you 
don't spend a lot of money/time running NLP on an unintentionally large selection of notes.

And with that, the natural language processing of notes is finished.
The rest of this guide will be about setting up a chart review for human comparison with NLP.

Importantly: re-run your [Cumulus AWS Glue crawler](https://docs.smarthealthit.org/cumulus/etl/setup/#create-tables-with-glue) 
at this point in order to pick up the newly created NLP tables and their schemas. Note
that as you run these tasks against _new models_, you will need to run this crawler again (though
only for the first time)

## 5. Generate NLP Highlights

Returning to the `cumulus-library`, we want to rebuild the study now that we have LLM response
tables in order to generate `irae__highlights_*` tables for each task. We could do this by 
re-running the whole study, or we could target a table-builder in particular using 
the `--builder` argument. Since we don't need to rebuild the whole study, we will do the latter 
to save time, targeting the following builders: 
1. `builder_irae_highlights_immunosuppressive_medications`. 
2. `builder_irae_highlights_multiple_transplant_history`. 
3. `builder_irae_highlights_donor`. 
4. `builder_irae_highlights_longitudinal`. 

### 5.a Immunosuppressive Medications against peri-operative notes
```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae \
  --builder builder_irae_highlights_immunosuppressive_medications
```

### 5.b History of Multiple Transplants against peri-operative notes
```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae \
  --builder builder_irae_highlights_multiple_transplant_history
```

### 5.c Donor Characteristics against peri-operative notes
```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae \
  --builder builder_irae_highlights_donor
```

### 5.d Outcome Variables against post-operative notes
```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae \
  --builder builder_irae_highlights_longitudinal
```

The resulting table, `irae__highlights`, formats LLM annotations to be digestible in
uploading notes to a label studio project. 


## 6. Configure Label Studio

For chart annotation, individual reviewers should have separate projects from each other 
to ensure blinding against other annotators responses. Additionally, each NLP task will have a
different UI configuration. Those config files can be found in `./docs/LS_interfaces`, 
with the `LS_*` prefix. For each annotator, for each one of the 4 NLP tasks above, 
we should do the following

- Install Label Studio according to [their docs](https://labelstud.io/guide/install.html).
- Create a new project, named however you like.
  - Skip the Data Import tab.
  - On the Label Setup tab, click "Custom template" on the bottom left and copy/paste the config
    file for this task. 

Once created, you will be looking at an empty project page. 
Take note of the new URL, you'll need to know the Label Studio project IDs later
(the number after `/projects/` in the URL).

## 7. Upload Highlighted Notes to Label Studio

For **every project** you've created you now need to upload highlighted notes. Review the Cumulus ETL 
[upload-notes docs](https://docs.smarthealthit.org/cumulus/etl/chart-review.html) as needed, but 
you'll want to run a variation of `upload-notes` with the following options:

### 7.a Immunosuppressive Medications against peri-operative notes 
```shell
docker compose run --rm \
  cumulus-etl upload-notes \
  <input folder with ndjson files from step K above> \
  <label studio url> \
  <your typical ETL PHI folder> \
  --philter=disable \
  --grouping none \
  --ls-project <PROJECT_ID_FOR_THIS_PERSON_X_TASK> \
  --ls-token <PATH_TO_LS_TOKEN> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae_highlights_immunosuppressive_medications \
  --label-by-athena-table irae_highlights_immunosuppressive_medications
```

### 7.b History of Multiple Transplants against peri-operative notes 
```shell
docker compose run --rm \
  cumulus-etl upload-notes \
  <input folder with ndjson files from step K above> \
  <label studio url> \
  <your typical ETL PHI folder> \
  --philter=disable \
  --grouping none \
  --ls-project <PROJECT_ID_FOR_THIS_PERSON_X_TASK> \
  --ls-token <PATH_TO_LS_TOKEN> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae_highlights_multiple_transplant_history \
  --label-by-athena-table irae_highlights_multiple_transplant_history
```

### 7.c Donor Characteristics against peri-operative notes 
```shell
docker compose run --rm \
  cumulus-etl upload-notes \
  <input folder with ndjson files from step K above> \
  <label studio url> \
  <your typical ETL PHI folder> \
  --philter=disable \
  --grouping none \
  --ls-project <PROJECT_ID_FOR_THIS_PERSON_X_TASK> \
  --ls-token <PATH_TO_LS_TOKEN> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae_highlights_donor \
  --label-by-athena-table irae_highlights_donor
```

### 7.d Outcome Variables against post-operative notes 
```shell
docker compose run --rm \
  cumulus-etl upload-notes \
  <input folder with ndjson files from step K above> \
  <label studio url> \
  <your typical ETL PHI folder> \
  --philter=disable \
  --grouping none \
  --ls-project <PROJECT_ID_FOR_THIS_PERSON_X_TASK> \
  --ls-token <PATH_TO_LS_TOKEN> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae_highlights_longitudinal \
  --label-by-athena-table irae_highlights_longitudinal
```

A few noteworthy comments on this command configuration: 
- `--philter=disable \` is included assuming that your chart-reviewers are 
  cleared to be reviewing PHI-rich notes. If you want to remove PHI before the 
  chart-review process, you should drop this argument. 
- Remember to pass any other required parameters like `--ls-project` and `--ls-token` 
  (from the linked docs above).
- If your DocumentReferences hold links to EHR resources (rather than inlined data),
  you will also need to pass the usual ETL `--fhir-url` flag and its related authentication flags.

Once this is done, go to your project page in Label Studio and you should see a lot of charts.

## 8. Have Subject-Matter Experts Review the Uploaded Charts

Give them access to Label Studio and have them annotate the charts! 
A few helpful links for chart-review guidance are:
- [User Guide Slide Show (Dec 16)](https://docs.google.com/presentation/d/1-exyUEOtZGDyK20ihPshFzbG-Tj3A3kH1fwCu3rUk_c/edit?slide=id.p#slide=id.p)
- [Detailed Chart Review Guidelines](https://docs.google.com/document/d/17lGRV3vN0C05QS3zZUR3oN8VfiGfpVNT8Va0_Wly6Eg/edit?tab=t.0)
- [Detailed Study Variables and Decision Criteria for Chart Reviewers](https://docs.google.com/document/d/1pQRG66C21X064Bnuci_v78mgfPfB6ox5sVA_ZqHfILI/edit?tab=t.0)