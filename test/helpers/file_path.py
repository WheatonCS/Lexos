import os
from os.path import join as path_join

__current_file_dir__ = dir_path = os.path.dirname(os.path.realpath(__file__))

TEST_SUITE_PATH = path_join(__current_file_dir__, '..', 'test_suite')


UPLOAD_TEST_SUITE_PATH = path_join(TEST_SUITE_PATH, 'Upload')

ENCODING_TEST_SUITE_PATH = path_join(UPLOAD_TEST_SUITE_PATH, 'encodings')
