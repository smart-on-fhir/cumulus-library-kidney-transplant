create or replace irae__doc_ontology as

with
kind as (select * from irae__doc_ontology_kind),
role as (select * from irae__doc_ontology_role),
smd as (select * from irae__doc_ontology_subjectmatterdomain),
service as (select * from irae__doc_ontology_typeofservice)
select kind.*
from
kind, smd
where kind.code = smd.code

