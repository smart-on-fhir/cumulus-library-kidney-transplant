from typing import Iterable

import cumulus_library
from cumulus_library import base_utils, databases
from cumulus_library.template_sql import sql_utils

from cumulus_library_kidney_transplant.tools import filetool


class IbdFlatteningMixin:
    """Mixin providing shared flattening logic for IBD wide-table builders.

    Combine with cumulus_library.BaseTableBuilder to create a concrete builder:

        class MyBuilder(
            cumulus_library.BaseTableBuilder,
            IbdFlatteningMixin,
            task_display="My Task",
            task_tabular_display="my_task",
        ):
            def _make_empty_query(self, config):
                ...
    """

    def __init_subclass__(cls, task_display="", task_tabular_display="", **kwargs):
        super().__init_subclass__(**kwargs)
        # Special variable for library builders
        cls.display_text = f"Flattening IBD {task_display} NLP..."

        # Other variables based on these keyword args
        # Progress text to display when checking possible source tables
        cls.progress_text = f"Discovering available NLP tables for IBD {task_display} variables..."

        # The common prefix across all source tables which vary by LLM deployment
        cls.src_table_prefix = f"ibd__nlp_{task_tabular_display.lower()}"

        # The ultimate destination table for the builder's resulting sql 
        # This name should also match the relevant jinja template
        cls.dest_table = f"ibd__llm_{task_tabular_display.lower()}_wide"

    @staticmethod
    def _is_table_valid(database: databases.DatabaseBackend, table_name: str) -> bool:
        """
        Check if a table is valid for use in the flattening process.
        The basic criteria for validity is that the table contains a 'result' column with non-empty results. Sub-classes can add more specific criteria by overriding this method.
        """        
        return sql_utils.is_field_present(
            database=database,
            source_table=table_name,
            source_col="result",
            expected={},
        )

    def _make_query_with_tables(self, tables: Iterable[str]):
        """
        Create a query that uses the specified tables and the template defined by the path
        to the llm template directory and the stem of the destination table.
        """
        return cumulus_library.get_template(
            self.dest_table,
            filetool.path_llm_template(),
            table_names=tables,
        )

    def _get_valid_ibd_nlp_tables(self, database: databases.DatabaseBackend) -> set[str]:
        """
        Get a set of all valid IBD NLP tables from the database.
        Checks a list of known source tables for LLMs we support.
        """
        source_tables = [
            f"{self.src_table_prefix}_claude_sonnet45",
            f"{self.src_table_prefix}_gpt51",
            f"{self.src_table_prefix}_gpt_oss_120b",
        ]
        valid_tables = set()
        with base_utils.get_progress_bar() as progress:
            task = progress.add_task(
                self.progress_text,
                total=len(source_tables),
            )
            for source_table in source_tables:
                if self._is_table_valid(database, source_table):
                    valid_tables.add(source_table)
                progress.advance(task)
        return valid_tables

    def _make_empty_query(self, config: cumulus_library.StudyConfig):
        """Return an appropriate empty query for this task.

        Subclasses must implement this. Called when no valid source tables are
        found so the destination table is still created with the correct schema.
        """
        raise NotImplementedError(f"{type(self).__name__} must implement _make_empty_query")

    def _make_query(self, config: cumulus_library.StudyConfig):
        valid_tables = self._get_valid_ibd_nlp_tables(config.db)
        if valid_tables:
            return self._make_query_with_tables(valid_tables)
        return self._make_empty_query(config)

    def prepare_queries(self, *args, config: cumulus_library.StudyConfig, **kwargs):
        self.queries.append(self._make_query(config=config))
