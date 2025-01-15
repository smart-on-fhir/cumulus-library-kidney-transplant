from typing import List
from cumulus_library_kidney_transplant import manifest, filetool
from cumulus_library.builders.counts import CountsBuilder
from cumulus_library_kidney_transplant.study_prefix import PREFIX

class Cube:
    from_table: str = None
    create_table: str = None
    col_list: List[str] = None
    builder = CountsBuilder(PREFIX)

    def __init__(self, create_table: str, from_table: str, col_list: List[str]):
        """
        The purpose of this class is to use `filetool.py` to write files for the study builder and
        provide basic information for `dashboard.py` to create a template. Use has been deprecated and may be ignored.

        :param create_table: name of the table in the CTAS statement (create `table` as )
        :param from_table: source table to compile the cube counts
        :param col_list: list of columns to include in the cube output
        """
        self.create_table = create_table
        self.from_table = from_table
        self.col_list = col_list

    def cnt_encounter(self):
        return filetool.save_athena_view(
            view_name=self.create_table,
            contents=self.builder.count_encounter(self.create_table, self.from_table, self.col_list))

    def cnt_patient(self):
        return filetool.save_athena_view(
            view_name=self.create_table,
            contents=self.builder.count_patient(self.create_table, self.from_table, self.col_list))
