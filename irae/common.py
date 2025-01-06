import os
import datetime
import csv
import json
from enum import Enum
from typing import List, Dict, Any, Iterable, Generator
from . import jsonifiers

###############################################################################
#
# Read/Write Text
#
###############################################################################
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

###############################################################################
#
# Read/Write JSON
#
###############################################################################
def read_json(json_file: str, encoding: str = 'UTF-8') -> Dict[Any, Any]:
    """
    Read json from file
    :param json_file: absolute path to file
    :param encoding: provided file's encoding
    :return: json file contents
    """
    with m_open(file=json_file, encoding=encoding) as j_file:
        return json.load(j_file)

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

###############################################################################
#
# Read/Write CSV
#
###############################################################################

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
