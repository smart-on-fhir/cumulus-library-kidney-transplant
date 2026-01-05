"""Module for generating donor IRAE NLP highlight tables"""

import pathlib

import cumulus_library
from cumulus_library import base_utils, databases
from cumulus_library.template_sql import sql_utils, base_templates


class IraeNlpHighlightsDonorBuilder(cumulus_library.BaseTableBuilder):
    display_text = "Transforming donor IRAE NLP results into a table of highlights..."

    @staticmethod
    def _is_table_valid(database: databases.DatabaseBackend, table_name: str) -> bool:
        valid = sql_utils.is_field_present(
            database=database,
            source_table=table_name,
            source_col="result",
            expected={},
        )
        # In addition to checking for the presence of a result column, we also want to check for the presence of donor_serostatus_mention data in the result column's schema. We will do this with a somewhat hacky query and a check that the resulting table_schema is not empty.
        query = cumulus_library.get_template(
            "result_column_schema_check",
            pathlib.Path(__file__).parent,
            schema_name=database.schema_name,
            table_names=[table_name],
            expected_column='donor_serostatus_mention',
        )
        try:
            table_schema = database.cursor().execute(query).fetchall()
        except database.operational_errors():
            table_schema = []
        return valid and table_schema != []

    def _get_valid_irae_nlp_tables(self, database: databases.DatabaseBackend) -> set[str]:
        source_tables = [
            "irae__nlp_donor_gpt4o",
            "irae__nlp_donor_gpt5",
            "irae__nlp_donor_gpt_oss_120b",
            "irae__nlp_donor_llama4_scout",
            "irae__nlp_donor_claude_sonnet45",
        ]
        valid_tables = set()
        with base_utils.get_progress_bar() as progress:
            task = progress.add_task(
                "Discovering available NLP tables for donor IRAE variables...",
                total=len(source_tables),
            )
            for source_table in source_tables:
                if self._is_table_valid(database, source_table):
                    valid_tables.add(source_table)
                progress.advance(task)
        return valid_tables

    def prepare_queries(
        self,
        *args,
        config: cumulus_library.StudyConfig,
        **kwargs,
    ):
        valid_tables = self._get_valid_irae_nlp_tables(config.db)
        query = cumulus_library.get_template(
            "irae__highlights_donor",
            pathlib.Path(__file__).parent,
            table_names=valid_tables,
        )
        self.queries.append(query)
