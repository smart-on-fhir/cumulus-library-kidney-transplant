### Checklist
- [ ] Consider if documentation needs to be updated
- [ ] Consider if tests should be added
- [ ] If your PR updates Pydantic, make sure you've done the following before finalizing your updates
  - [ ] For schemas that have changed, update impacted task versions in **SQL template files**
  - [ ] For schemas that have changed, update impacted task versions in **cumulus_library_kidney_transplant/nlp_clinical_peri_tasks.toml** and **cumulus_library_kidney_transplant/nlp_clinical_post_tasks.toml**
  - [ ] `python cumulus_library_kidney_transplant/llm/create_model_summary.py`
  - [ ] `python cumulus_library_kidney_transplant/llm/create_schema.py`
  - [ ] `python cumulus_library_kidney_transplant/llm/create_wide_sql_examples.py`