from typing import List
from fhirclient.models.coding import Coding
from irae import resources
from irae.variable.base import Vocab
from irae.variable.base import BinaryClass, MultiClass

class SpreadsheetReader:
    filename = None
    alias = None
    vocab: Vocab = None

    def __init__(self, filename: str, alias: str, vocab=Vocab.ICD10CM):
        """
        :param filename: researcher provided/uploaded spreadsheet
        :param alias: variable name like "suicidality"
        :param vocab: default vocabulary to apply, many/most researchers start with ICD10CM
        """
        self.filename = filename
        self.alias = alias
        self.vocab = vocab

    def read_coding_list(self, delimiter: str = ',', quote_char: str = '"') -> List[Coding]:
        codes = list()

        for columns in resources.read_csv(self.filename, delimiter, quote_char):
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

        for columns in common.read_csv(self.filename, '\t'):
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
