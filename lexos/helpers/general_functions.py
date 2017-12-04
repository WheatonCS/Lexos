import errno
import os
import pickle
import re
import shutil
from typing import Union, Any
from zipfile import ZipFile

import chardet
import markupsafe

import lexos.helpers.constants as constants
from lexos.helpers.exceptions import LexosException


def get_encoding(input_string: bytes) -> str:
    """Uses chardet to return the encoding type of a string.

    :param input_string: A string.
    :return: The string's encoding type.
    """
    encoding_detect = chardet.detect(input_string[
                                     :constants.MIN_ENCODING_DETECT])
    encoding_type = encoding_detect['encoding']
    return encoding_type


def make_preview_from(input_string: str) -> str:
    """Creates a formatted preview string from a file contents string.

    :param input_string: A string from which to create the formatted preview.
    :return: The formatted preview string.
    """
    if len(input_string) <= constants.PREVIEW_SIZE:
        preview_string = input_string
    else:
        newline = '\n'
        half_length = constants.PREVIEW_SIZE // 2
        preview_string = input_string[:half_length] + '\u2026 ' + newline + \
            newline + '\u2026' + input_string[-half_length:]  # New look
    return preview_string


def generate_d3_object(word_counts: dict, object_label: str,
                       word_label: str, count_label: str) -> object:
    """Generates a properly formatted JSON object for d3 use.

    :param word_counts: dictionary of words and their count
    :param object_label: The label to identify this object.
    :param word_label: A label to identify all "words".
    :param count_label: A label to identify all counts.
    :return: The formatted JSON object.
    """
    json_object = {'name': str(object_label), 'children': []}

    for word, count in list(word_counts.items()):
        json_object['children'].append({word_label: word, count_label: count})
    return json_object


def zip_dir(directory: str, zip_handler: ZipFile):
    """zip all the file in path into a zipfile type ziph

    :param directory: The directory that you want to zip
    :param zip_handler: the zipfile to put the zip information in.
    """
    cur_dir = os.getcwd()  # record current path
    os.chdir(directory)  # go to the path that need to be zipped
    # ziph is zipfile handle
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            zip_handler.write(os.path.join(root, file))
    os.chdir(cur_dir)  # go back to the original path


def copy_dir(src_dir: str, dst_dir: str):
    """copy all the file from src directory to dst directory

    :param src_dir: the source dir
    :param dst_dir: the destination dir
    """
    try:
        shutil.copytree(src_dir, dst_dir)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src_dir, dst_dir)
        else:
            raise FileNotFoundError('source dir does not exists')


def html_escape_deprec(input_string: str) -> str:
    """escape all the html content

    function deprecated, use markupsafe.escape
    :param input_string: A string that may contain html tags
    :return: the string with all the html syntax escaped so that it will be
    safe to put the returned string to html
    """
    return markupsafe.escape(input_string)


def apply_function_exclude_tags(input_string: str, functions: list) -> str:
    """strips the given text and apply the given functions

    :param input_string: string to strip
    :param functions: a list of functions to apply to input_string
    :return: striped text
    """
    striped_text = ''
    tag_pattern = re.compile(r'<.+?>', re.UNICODE | re.MULTILINE)
    tags = re.findall(tag_pattern, input_string)
    contents = re.split(tag_pattern, input_string)
    for i in range(len(tags)):
        for function_to_apply in functions:
            contents[i] = function_to_apply(contents[i])
        striped_text += contents[i]
        striped_text += tags[i]
    for function_to_apply in functions:
        contents[-1] = function_to_apply(contents[-1])
    striped_text += contents[-1]
    return striped_text


def _try_decode_bytes_(raw_bytes: bytes) -> str:
    """helper function for decode_byte,try to decode the raw bytes

    :param raw_bytes: the bytes you get and want to decode to string
    :return: A decoded string
    """
    # Detect the encoding with only the first couple of bytes
    encoding_detect = chardet.detect(
        raw_bytes[:constants.MIN_ENCODING_DETECT])
    # get the encoding
    encoding_type = encoding_detect['encoding']

    if encoding_type is None:
        encoding_detect = chardet.detect(raw_bytes)
        encoding_type = encoding_detect['encoding']

    try:
        # try to decode the string using the encoding we get
        decoded_string = raw_bytes.decode(encoding_type)

    except UnicodeDecodeError:
        # if decoding failed, we use all the bytes to detect encoding
        encoding_detect = chardet.detect(raw_bytes)
        encoding_type = encoding_detect['encoding']
        decoded_string = raw_bytes.decode(encoding_type)

    return decoded_string


def decode_bytes(raw_bytes: Union[bytes, str]) -> str:
    """Decodes raw bytes from a user's file into a string.

    :param raw_bytes: The bytes to be decoded to a python string.
    :return: The decoded string.
    """

    if isinstance(raw_bytes, bytes):
        try:
            decoded_str = _try_decode_bytes_(raw_bytes)

        except (UnicodeDecodeError, TypeError):
            raise LexosException('chardet fail to detect encoding of your '
                                 'file, please make sure your file is in '
                                 'utf-8 encoding')
    else:
        decoded_str = raw_bytes

    return decoded_str


def write_file_to_disk(contents: Any, dest_folder: str, filename: str):
    """Stores data in a file on the disk.

    :param contents: Whatever the file should contain.
    :param dest_folder: The directory path where the file should be saved.
    :param filename: The name of the file to be created.
    """

    try:
        os.makedirs(dest_folder)
    except FileExistsError:
        pass
    pickle.dump(contents, open(dest_folder + filename, 'wb'))


def load_file_from_disk(loc_folder: str, filename: str) -> Any:
    """Loads a file that was previously saved to the disk.

    :param loc_folder: The location of the containing folder.
    :param filename: The name of the file to be loaded.
    :return: The contents of the loaded file.
    """

    file_string = pickle.load(open(loc_folder + filename, 'rb'))
    return file_string
