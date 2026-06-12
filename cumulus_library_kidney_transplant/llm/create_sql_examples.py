from pathlib import Path

import cumulus_library

from cumulus_library_kidney_transplant.tools import filetool
from cumulus_library_kidney_transplant.llm.builder import (
    # Wide Table Builders
    IraeNlpDonorFlattenedBuilder,
    IraeNlpImmunosuppressiveMedicationsFlattenedBuilder,
    IraeNlpLongitudinalFlattenedBuilder,
    IraeNlpMultipleTransplantHistoryFlattenedBuilder,
    # Highlights Table Builders
    IraeNlpDonorHighlightsBuilder,
    IraeNlpImmunosuppressiveMedicationsHighlightsBuilder,
    IraeNlpLongitudinalHighlightsBuilder,
    IraeNlpMultipleTransplantHistoryHighlightsBuilder,
)

def make(builder: cumulus_library.BaseTableBuilder, nlp_model='gpt_oss_120b') -> Path:
    """
    :param builder: IBD Wide Table Builder
    :return: Path to SQL
    """
    print('Creating example SQL for:', builder.dest_table)
    nlp_origin = f"{builder.src_table_prefix}_{nlp_model}"
    query = builder._make_query_with_tables(tables=[nlp_origin])

    return filetool.save_llm_athena(f"{builder.dest_table}.sql", query)

def make_all_wide():
    return [
        make(IraeNlpDonorFlattenedBuilder()),
        make(IraeNlpImmunosuppressiveMedicationsFlattenedBuilder()),
        make(IraeNlpLongitudinalFlattenedBuilder()),
        make(IraeNlpMultipleTransplantHistoryFlattenedBuilder()),
    ]
def make_all_highlights():
    return [
        make(IraeNlpDonorHighlightsBuilder()),
        make(IraeNlpImmunosuppressiveMedicationsHighlightsBuilder()),
        make(IraeNlpLongitudinalHighlightsBuilder()),
        make(IraeNlpMultipleTransplantHistoryHighlightsBuilder()),
    ]

if __name__ == "__main__":
    make_all_wide()
    make_all_highlights()
