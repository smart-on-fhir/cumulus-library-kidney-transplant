import os
import datetime
import csv
import json
from enum import Enum
from typing import List, Dict, Any, Iterable, Generator
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.coding import Coding
from . import jsonifiers

###############################################################################
#
# Type Check (yes/no)
#
###############################################################################
def is_enum(obj) -> bool:
    return isinstance(obj, Enum)

def is_list(obj) -> bool:
    return isinstance(obj, list)

def is_list_type(obj, type) -> bool:
    if isinstance(obj, list) and all(isinstance(item, type) for item in obj):
        return True
    return False

###############################################################################
#
# Guard input types, fail fast
#
###############################################################################
def guard_list(obj) -> list:
    if isinstance(obj, list):
        return obj
    return [obj]

def guard_range(obj) -> range:
    print(f'guard_range : {obj}')
    if isinstance(obj, list):
        return range(obj[0], obj[1])
    if isinstance(obj, tuple):
        return range(obj[0], obj[1])
    if isinstance(obj, range):
        return obj

    Exception(f'guard_range failed for {obj}')

def as_coding_list(obj) -> List[Coding]:
    obj = guard_list(obj)

    if is_list_type(obj, Coding):
        return obj

    return [as_coding(c) for c in list(obj)]

def as_coding(obj) -> Coding:
    c = Coding()
    src = obj.__dict__
    c.code = src.get('code')
    c.display = src.get('display')
    c.system = src.get('system')
    return c

###############################################################################
#
# Collection safety
#
###############################################################################
def uniq(unsorted: Iterable) -> List:
    """
    :param unsorted: list of header names
    :return: sorted list of unique header names
    """
    return sorted(list(set(unsorted)))

###############################################################################
#
# Read/Write Text/Json
#
###############################################################################
def m_open(**kwargs):
    """
    Wrapper for built in open with exception handling and logging
    :return: file like object
    """
    try:
        return open(**kwargs)
    except Exception:
        print('m_open raised an exception', exc_info=True)
        raise

def read_text(text_file: str, encoding: str = 'UTF-8') -> str:
    """
    Read text from file
    :param text_file: absolute path to file
    :param encoding: provided file's encoding
    :return: file text contents
    """
    with m_open(file=text_file, encoding=encoding) as t_file:
        return t_file.read()


def write_text(contents: str, file_path: str, encoding: str = 'UTF-8') -> str:
    """
    Write file contents
    :param contents: string contents
    :param file_path: absolute path of target file
    :param encoding: provided file's encoding
    :return: text_file name
    """
    with m_open(file=file_path, mode='w', encoding=encoding) as file_path:
        file_path.write(contents)
        file_path.close()
        return file_path.name


def write_bytes(data: str, file_path: str) -> None:
    """
    Writes provided bytes to provided file path
    :param data: bytes contents
    :param file_path: absolute path to file
    :return:
    """
    with m_open(file=file_path, mode='wb') as bytes_file:
        bytes_file.write(data.encode('UTF-8'))


def read_bytes(binary_file: str) -> bytes:
    """
    Read bytes from binary file
    :param binary_file: absolute path to file
    :return: bytes file contents
    """
    with m_open(file=binary_file, mode='rb') as bin_file:
        return bytes(bin_file.read())


def write_json(contents: Dict[Any, Any], json_file_path: str, encoding: str = 'UTF-8') -> str:
    """
    Write JSON to file
    :param contents: json (dict) contents
    :param json_file_path: absolute destination file path
    :param encoding: provided file's encoding
    :return: file name
    """
    directory = os.path.dirname(json_file_path)
    os.makedirs(directory, exist_ok=True)
    with m_open(file=json_file_path, mode='w', encoding=encoding) as json_file_path:
        json.dump(contents, json_file_path, indent=4, cls=jsonifiers.CustomJsonEncoder)
        return json_file_path.name


def read_json(json_file: str, encoding: str = 'UTF-8') -> Dict[Any, Any]:
    """
    Read json from file
    :param json_file: absolute path to file
    :param encoding: provided file's encoding
    :return: json file contents
    """
    with m_open(file=json_file, encoding=encoding) as j_file:
        return json.load(j_file)

def write_csv(rows: Iterable[List[str]], file_csv: str, delimiter: str = ',', quote_char: str = '"'):
    """Write csv file.
    :param rows: The contents to write to file.
    :param file_csv: absolute path to the csv
    :param delimiter: the delimiter used in the csv
    :param quote_char: the quote character used in the csv
    :return: an iterator of row values
    """
    with open(file_csv, 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quote_char)

        for row in rows:
            writer.writerow(row)


def read_csv(file_csv: str, delimiter: str = ',', quote_char: str = '"') -> Generator[List[str], None, None]:
    """
    Parse csv file
    :param file_csv: absolute path to the csv
    :param delimiter: the delimiter used in the csv
    :param quote_char: the quote character used in the csv
    :return: an iterator of row values
    """
    with m_open(file=file_csv) as csv_file:
        for row in csv.reader(csv_file, delimiter=delimiter, quotechar=quote_char):
            yield row


def list_from_csv_column(file_csv: str, column: str, delimiter: str = ',', quote_char: str = '"') -> List[str]:
    """
    Parses csv file and returns all values from the provided column
    :param file_csv: absolute path to the csv
    :param column: the column from which to gather values
    :param delimiter: the delimiter used in the csv
    :param quote_char: the quote character used in the csv
    :return: a list of all values from the requested column
    """
    return [row[column] for row in read_csv(file_csv=file_csv, delimiter=delimiter, quote_char=quote_char)]


###############################################################################
#
# Helper Functions: date and time
#
###############################################################################

def parse_fhir_date(yyyy_mm_dd) -> FHIRDate:
    """
    :param yyyy_mm_dd: YEAR Month Date
    :return: FHIR Date with only the date part.
    """
    if yyyy_mm_dd and isinstance(yyyy_mm_dd, FHIRDate):
        return yyyy_mm_dd
    if yyyy_mm_dd and isinstance(yyyy_mm_dd, str):
        if len(yyyy_mm_dd) >= 10:
            yyyy_mm_dd = yyyy_mm_dd[:10]
            return FHIRDate(yyyy_mm_dd)

def parse_date(value: str | None) -> datetime.date | None:
    return parse_datetime(value).date()

def parse_datetime(value: str | None) -> datetime.datetime | None:
    """
    Converts FHIR instant/dateTime/date types into a Python format.

    - This tries to be very graceful - any errors will result in a None return.
    - Missing month/day fields are treated as the earliest possible date (i.e. '1')

    CAUTION: Returned datetime might be naive - which makes more sense for dates without a time.
             The spec says any field with hours/minutes SHALL have a timezone.
             But fields that are just dates SHALL NOT have a timezone.
    """
    if not value:
        return None

    try:
        # Handle partial dates like "1980-12" (which spec allows, but fromisoformat can't handle)
        pieces = value.split("-")
        if len(pieces) == 1:
            return datetime.datetime(int(pieces[0]), 1, 1)  # note: naive datetime
        elif len(pieces) == 2:
            return datetime.datetime(int(pieces[0]), int(pieces[1]), 1)  # note: naive datetime

        # Until we depend on Python 3.11+, manually handle Z
        value = value.replace("Z", "+00:00")

        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return None

def datetime_now(local: bool = False) -> datetime.datetime:
    """
    Current date and time, suitable for use as a FHIR 'instant' data type

    The returned datetime is always 'aware' (not 'naive').

    :param local: whether to use local timezone or (if False) UTC
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    if local:
        now = now.astimezone()
    return now

