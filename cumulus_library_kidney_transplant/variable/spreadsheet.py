from typing import List
from enum import Enum
from pathlib import Path
from fhirclient.models.coding import Coding
from cumulus_library_kidney_transplant import filetool
from cumulus_library_kidney_transplant.vocab import Vocab
from cumulus_library_kidney_transplant.variable.deprecated import BinaryClass, MultiClass

class Delimiter(Enum):
    csv = ','
    tsv = '\t'
    pipe = '|'

class SpreadsheetReader:
    filename = None
    alias = None
    vocab: Vocab = None
    delimiter: Delimiter = None

    def __init__(self, filename: Path | str, alias: str, vocab: Vocab, delimiter: Delimiter):
        """
        :param filename: researcher provided/uploaded spreadsheet
        :param alias: variable name like "suicidality"
        :param vocab: default vocabulary to apply, many/most researchers start with ICD10CM
        """
        self.filename = filename
        self.alias = alias
        self.vocab = vocab
        self.delimiter = delimiter

    def read_coding_list(self, quote_char: str = '"') -> List[Coding]:
        codes = list()

        for columns in filetool.read_csv(self.filename, self.delimiter.value, quote_char):
            c = Coding()
            c.code = columns[0]
            c.display = columns[1]
            c.system = self.vocab
            codes.append(c)
        return codes

    def read_binaryclass(self):
        return BinaryClass(self.alias, self.read_coding_list())

    def read_multiclass(self):
        parsed = dict()
        for columns in filetool.read_csv(self.filename, self.delimiter.value):
            code = columns[0]
            display = columns[1]
            subtype = columns[2]

            if subtype not in parsed.keys():
                parsed[subtype] = list()

            parsed[subtype].append((code, display))

        multiclass = MultiClass(self.alias)

        for subtype in parsed.keys():
            if subtype not in multiclass.subtypes.keys():
                multiclass.subtypes[subtype] = BinaryClass(subtype)

            for item in parsed[subtype]:
                [code, display] = item
                c = Coding()
                c.code = code
                c.display = display
                c.system = self.vocab

                multiclass.subtypes[subtype].concepts.append(c)
        return multiclass
