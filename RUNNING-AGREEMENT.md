# Establishing Annotator Agreement on Donor Variables

This guide will walk you through establishing the level of annotator agreement between human
chart reviewers and other chart reviewers, as well as between human annotators and LLMs. 
Specifically, each site will have multiple (>= 2) chart reviewers annotate 100 notes for 
donor characteristic variables from scratch, without LLM predictions. By comparing 
the annotations between reviewers and eventually between reviewers and LLMs, we can:

- Establish the annotator agreement between chart reviewers on our task, starting from blank notes;
- Establish the annotators agreement scores compared against LLM-generated annotations; and 
- (Hopefully) Demonstrate that annotators have similar agreement between the LLM and between each 
  other, rejoicing if the agreement with the LLM responses is greater than between reviewers alone 


The guide's steps break down as follows: 
1. Build the kidney study using `cumulus-library build`.
2. Sample from our cohort for 100 notes using Athena.
3. Upload those notes to labelstudio projects for chart reviewers using `cumulus-etl upload-notes`.
4. Have chart reviewers annotate those notes using labelstudio.
5. Run Donor-task NLP for those 100 notes using `cumulus-etl nlp` and 
   generate highlights for LS using `cumulus-library build`.
6. Calculate agreement scores using `chart-review`.


## Prerequisites

- Familiarity with running [chart-review](https://docs.smarthealthit.org/cumulus/chart-review/)
- An existing Cumulus stack, with an already-built `core` study.
  - See the general [Cumulus documentation](https://docs.smarthealthit.org/cumulus/)
    for setting that up.
- Familiarity with [creating new cumulus library studies](https://docs.smarthealthit.org/cumulus/library/creating-studies.html#creating-library-studies)
- Familiarity with [running NLP workflows using cumulus etl](https://docs.smarthealthit.org/cumulus/etl/nlp/example.html)
- This module should be installed in the same python environment as the cumulus stack. This can 
  be done by running `pip install cumulus-library-kidney-transplant`, which will add 
  an `irae` target to `cumulus-library`.
- **Lastly, make sure that your cloud environment has been updated to use the**
  **[latest set of DeltaTables](https://github.com/smart-on-fhir/cumulus-etl/blob/main/docs/setup/cumulus-aws-template.yaml).**
  **To support these numerous new tasks, new tables have been introduced.**


## 1 - Build the Kidney Study

First we want to build our cohort of interest with this kidney study 
and [cumulus-library](https://docs.smarthealthit.org/cumulus/library/) like so: 
```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae 
```

We will use the `irae__sample_casedef_index_100` tables we just created to sample for some notes of interest.


## 2 Sample and Unarchive Notes 

Sites will have their own bespoke process for translating notes identified in the aforementioned Athena table into 
unarchived copies of the notes text, PHI and all. One helpful query for formatting the information of interest: 

```sql
SELECT DISTINCT 
	subject_ref,
	encounter_ref,
	documentreference_ref
FROM 
   irae__sample_casedef_index_100
ORDER BY
	documentreference_ref
LIMIT 100;
```

If your site needs the `group_name` field that Athena provides in your archiving process and your system has a 
many-to-many relationship between patients and groups, we've found the following query useful: 

```sql
SELECT 
	documentreference_ref, 
	subject_ref, 
	encounter_ref, 
	MAX(group_name) as group_name
FROM irae__sample_casedef_index_100
GROUP BY 
	documentreference_ref, 
	subject_ref, 
	encounter_ref
ORDER BY 
	documentreference_ref
LIMIT 100
```

With these notes identified, gather DocumentReference ndjson from your EHR. You can either 
re-export the documents of interest, or use ndjson from a previous export. Ideally these notes are 
pre-inlined with clinical note content, as this will save time/hassle re-downloading the notes 
every time we run NLP. If you're gathering notes using our `smart-fetch` tool the notes should be 
[inlined automatically when exporting](https://docs.smarthealthit.org/cumulus/fetch/hydration.html#inlining-clinical-notes).

Place the ndjson in a folder, and take note of the paths to these notes for later steps.


## 3 Upload to Label Studio 

For chart annotation, individual reviewers should have separate projects from each other to 
ensure blinding against other annotators responses. For this agreement task, you should use 
the `LS_DONOR` config file in this project. For each annotator, we should do the following

- Install Label Studio according to [their docs](https://labelstud.io/guide/install.html).
- Create a new project, named however you like - probably something related to annotator agreement`.
  - Skip the Data Import tab.
  - On the Label Setup tab, click "Custom template" on the bottom left and copy/paste the 
    donor config file for this task. 

Once created, you will be looking at an empty project page.  Take note of the new URL, you'll need 
to know the Label Studio project IDs later (the number `/projects/<NUM>` in the URL). From here, 
we need to populate the project with the notes we've just unarchived.

```shell
docker compose run --rm \
  cumulus-etl upload-notes \
  <input folder with ndjson files from step 2 above> \
  <label studio url> \
  <your typical ETL PHI folder> \
  --philter=disable \
  --grouping none \
  --ls-project <PROJECT_ID_FOR_THIS_PERSON_X_TASK> \
  --ls-token <PATH_TO_LS_TOKEN> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> 
```

While doing this, set aside one more project than you have annotators. This will be used later to 
create data we can use to compare LLM predictions against human chart-review annotations.


## 4 Annotate 

Give chart reviewers access to Label Studio and have them annotate the charts! Unlike for 
other tasks, the goal of this exercise is to annotate EVERY note in order to establish 
annotator agreement. The following 
[User Guide Slide Show (Dec 16)](https://docs.google.com/presentation/d/1-exyUEOtZGDyK20ihPshFzbG-Tj3A3kH1fwCu3rUk_c/edit?slide=id.p#slide=id.p) 
is helpful for this annotation process.


## 5 Run Donor NLP Task

In parallel to human annotation, we want to generate some LLM-based annotations for this task. 
For the 100 notes previously idenfitied, run: 

```sh
docker compose run --rm -it\
  cumulus-etl nlp \
  --task irae__nlp_donor_gpt_oss_120b_OR_WHATEVER_MODEL_YOU_ARE_USING \
  <input folder with ndjson files from step 2 above> \
  <your typical ETL PHI folder> \
  <your typical ETL OUTPUT folder> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> 
```

Importantly: re-run your [Cumulus AWS Glue crawler](https://docs.smarthealthit.org/cumulus/etl/setup/#create-tables-with-glue) 
at this point in order to pick up the newly created NLP table and it's schema. Note
that if you run tasks against _new models_, you will need to run this crawler again (though
only for the first time).

After you've run the task and rerun Glue crawlers, 
we want to transform these LLM responses into a format that can be 
used to populate a labelstudio project. We will do this 
by using a specific builder identified in our kidney study. 

```sh
cumulus-library build \
  --database <relevant_cumulus_library_database> \
  --workgroup <relevant_cumulus_library_workgroup> \
  --profile <relevant_cumulus_library_profile> \
  -t irae \
  --builder builder_irae_highlights_donor
```

This will produce a `irae__highlights_donor` table for future use. Note that 
if you run `cumulus-library clean -t irae`, this table will be deleted. Keep that in mind
when cleaning up your study environments in Athena.


## 6 Calculate Agreement 

Finally, we need to calculate the agreement between annotators - comparing human to human, 
and LLM to human - using the `chart-review` package. As of chart-review version 2.4.1, multiple 
labelstudio files can be used to describe annotations across different annotators. 


### Agreement Between Human Chart Reviewers

To compare our human annotators, export labelstudio-export from each annotator's unique project 
and move those files into the same directory. Inspect the export files for the unique ID's 
associated with each annotator. Then create a `config.yaml` file naming the annotators accordingly. 
For example, if I had two export files - one from Andy's project with `completed_by` id = 2, and 
one from Dylan's project with `completed_by` id = 4 - I would create 
the following `config.yaml` file: 

```yaml
annotators:
  andy: 2
  dylan: 4
```

To avoid computing agreement on irrelevant labels (e.g. `FlagReview`), we will specify which 
labels and sublabels we want to compare using the `labels` field in our yaml config. Adding 
to our previous config, we should now have: 

```yaml
annotators:
  andy: 2
  dylan: 4

labels:  
  - Transplant Date | *
  - Donor Type | *
  - Donor Relationship | *
  - Hla Match Quality | *
  - Hla Mismatch Count | *
  - Donor Serostatus | *
  - Donor Serostatus EBV | *
  - Donor Serostatus CMV | *
  - Recipient Serostatus | *
  - Recipient Serostatus EBV | *
  - Recipient Serostatus CMV | *
```

Now run `chart-review accuracy` and record the reported value for Cohen's Kappa: 

```sh
chart-review accuracy andy dylan
```

Since all we're concerned with is Cohen's Kappa, the order of which annotations are ground truth 
and which are the comparing annotator doesn't matter. 

### Agreement Between Humans and LLM 

Apologies in advance for this part...

The lowest tech solution to this right now is circuitous: 
- Upload these predictions to a new labelstudio project;
- Manually confirm all the annotations (this can be expedited by the use of shortcuts – 
  CMD/CTRL + Enter for approving the LLM suggested annotations; 
  then Shift + Down arrow to move to the next task in the sequence);
- Export the confirmed annotations;
- Manually modify the `completed_by` id to an unused ID - `999` should hopefully work. This 
  can be done with a global find and replace of the current `completed_by` id.
- Update your config.yaml file to include this annotator as your LLM. 

To upload the predictions to a labelstudio project, we'll follow the same steps as above in 3, 
with some additional `label-by-athena-table` and `select-by-athena-table` arguments in order 
to populate the notes with the highlights generated in 5: 

```sh
docker compose run --rm \
  cumulus-etl upload-notes \
  <input folder with ndjson files from step K above> \
  <label studio url> \
  <your typical ETL PHI folder> \
  --philter=disable \
  --grouping none \
  --ls-project <PROJECT_ID_FOR_THE_EXTRA_LS_PROJECT> \
  --ls-token <PATH_TO_LS_TOKEN> \
  --athena-database <relevant_cumulus_library_database> \
  --athena-workgroup <relevant_cumulus_library_workgroup> \
  --select-by-athena-table irae_highlights_donor \
  --label-by-athena-table irae_highlights_donor
```

Once you've gone through, manually confirmed all the LLM predictions, exported the LabelStudio 
Export file, and manually modified the `completed_by` id in the file to some unused ID, 
the final step is to add this annotator to your `config.yaml` file. Continuing from 
our earlier example, our new file would be: 

```yaml
annotators:
  andy: 2
  dylan: 4
  llm: 999

labels:  
  - Transplant Date | *
  - Donor Type | *
  - Donor Relationship | *
  - Hla Match Quality | *
  - Hla Mismatch Count | *
  - Donor Serostatus | *
  - Donor Serostatus EBV | *
  - Donor Serostatus CMV | *
  - Recipient Serostatus | *
  - Recipient Serostatus EBV | *
  - Recipient Serostatus CMV | *
```

Now run `chart-review accuracy` and record the reported value for Cohen's Kappa: 

```sh
chart-review accuracy andy llm
chart-review accuracy dylan llm
```

