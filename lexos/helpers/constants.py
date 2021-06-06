import getpass
import os


# Configurations
IS_SERVER = False
DUMPING = True


# File directories
FILE_CONTENTS_FOLDER = "filecontents/"
RESULTS_FOLDER = "analysis_results/"
WORKSPACE_DIR = "workspace/"
TMP_FOLDER = os.path.expanduser(
    "~\\AppData\\Local\\Temp") if os.name == "nt" else "/tmp/"
UPLOAD_FOLDER = os.path.join(TMP_FOLDER, "Lexos_" + str(getpass.getuser()))
CACHE_FOLDER = os.path.join(UPLOAD_FOLDER, "cache/")
RESOURCE_DIR = "resources/"


# File names
FILEMANAGER_FILENAME = "filemanager.p"
SESSION_FILENAME = "session.p"
FILE_INFORMATION_FIGNAME = "statistic.svg"
CORPUS_INFORMATION_FIGNAME = "corpus_statistic.svg"
WORKSPACE_FILENAME = "workspace.lexos"
MALLET_INPUT_FILE_NAME = "topicfile"
MALLET_OUTPUT_FILE_NAME = "topicfile_for_json"
TOPWORD_CSV_FILE_NAME = "topwordResult.csv"
DEBUG_LOG_FILE_NAME = "debug.log"
MUFI_3_FILENAME = "MUFI_3_DICT.tsv"
MUFI_4_FILENAME = "MUFI_4_DICT.tsv"
STOPWORD_FILENAME = "stopwords.p"
LEMMA_FILENAME = "lemmas.p"
CONSOLIDATION_FILENAME = "consolidations.p"
SPECIAL_CHAR_FILENAME = "specialchars.p"
DIGIT_MAP_FILENAME = "digitmap.p"
PUNCTUATION_MAP_FILENAME = "punctuationmap.p"
AMPERSAND_FILENAME = "ampersand.p"
HYPHEN_FILENAME = "hyphen.p"


# Numbers
MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB
MAX_FILE_SIZE_INT = 250
MAX_FILE_SIZE_UNITS = "M"
PREVIEW_SIZE = 255
MIN_ENCODING_DETECT = 10000
MIN_NEWLINE_DETECT = 1000
CHARACTERS_PER_LINE_IN_LEGEND = 100
ROUND_DIGIT = 4
SIM_QUERY_ROUND = 5


# Keys
FILEMANAGER_KEY = ""
SESSION_KEY = ""
FILE_CONTENT_KEY = ""


# General Settings
GENERALSETTINGS = "theme"


# General
DEFAULT_GENERALSETTINGS_OPTIONS = {
    "theme": "Basil Light"
}

# Docx Upload
WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/' \
                 'main}'
WORD_PICTURE = '{http://schemas.openxmlformats.org/drawingml/2006/picture}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
ROW = WORD_NAMESPACE + 'tr'
COL = WORD_NAMESPACE + 'tc'
BR = WORD_NAMESPACE + 'pPr'
DOC = WORD_NAMESPACE + 'document'
BODY = WORD_NAMESPACE + 'body'
DRAW = WORD_NAMESPACE + 'drawing'
PIC = WORD_PICTURE + 'cNvPr'
TAB = WORD_NAMESPACE + 'tab'
CHART = '{http://schemas.openxmlformats.org/drawingml/2006/' \
        'wordprocessingDrawing}' + 'docPr'
FALLBACK = '{http://schemas.openxmlformats.org/markup-compatibility/2006}' + \
           'Fallback'

# Scrub
SCRUBBOXES = (
    "keep_ampersands",
    "keep_apostrophes",
    "remove_digits",
    "keep_hyphens",
    "make_lowercase",
    "remove_newlines",
    "remove_punctuation",
    "remove_spaces",
    "remove_tabs",
    "scrub_tags",
    "stop_words_method",
)

SCRUBINPUTS = (
    "stop_words",
    "special_characters",
    "consolidations",
    "lemmas"
)

OPTUPLOADNAMES = (
    "stop_words_file[]",
    "lemmas_file[]",
    "consolidations_file[]",
    "special_characters_file[]"
)


# Unicode punctuation
UNICODE_PUNCT = "-=_!\"#%&*{},./:;?()[]@\\$^*+<>~`"\
                "\u00a1\u00a7\u00b6\u00b7\u00bf\u037e\u0387\u055a-"\
                "\u055f\u0589\u05c0\u05c3\u05c6\u05f3\u05f4\u0609"\
                "\u060a\u060c\u060d\u061b\u061e\u061f\u066a-\u066d"\
                "\u06d4\u0700-\u070d\u07f7-\u07f9\u0830-\u083e\u085e"\
                "\u0964\u0965\u0970\u0af0\u0df4\u0e4f\u0e5a\u0e5b"\
                "\u0f04-\u0f12\u0f14\u0f85\u0fd0-\u0fd4\u0fd9\u0fda"\
                "\u104a-\u104f\u10fb\u1360-\u1368\u166d\u166e\u16eb-"\
                "\u16ed\u1735\u1736\u17d4-\u17d6\u17d8-\u17da\u1800-"\
                "\u1805\u1807-\u180a\u1944\u1945\u1a1e\u1a1f\u1aa0-"\
                "\u1aa6\u1aa8-\u1aad\u1b5a-\u1b60\u1bfc-\u1bff\u1c3b"\
                "-\u1c3f\u1c7e\u1c7f\u1cc0-\u1cc7\u1cd3\u2016\u2017"\
                "\u2020-\u2027\u2030-\u2038\u203b-\u203e\u2041-"\
                "\u2043\u2047-\u2051\u2053\u2055-\u205e\u2cf9-\u2cfc"\
                "\u2cfe\u2cff\u2d70\u2e00\u2e01\u2e06-\u2e08\u2e0b"\
                "\u2e0e-\u2e16\u2e18\u2e19\u2e1b\u2e1e\u2e1f\u2e2a-"\
                "\u2e2e\u2e30-\u2e39\u3001-\u3003\u303d\u30fb\ua4fe"\
                "\ua4ff\ua60d-\ua60f\ua673\ua67e\ua6f2-\ua6f7\ua874-"\
                "\ua877\ua8ce\ua8cf\ua8f8-\ua8fa\ua92e\ua92f\ua95f"\
                "\ua9c1-\ua9cd\ua9de\ua9df\uaa5c-\uaa5f\uaade\uaadf"\
                "\uaaf0\uaaf1\uabeb\ufe10-\ufe16\ufe19\ufe30\ufe45"\
                "\ufe46\ufe49-\ufe4c\ufe50-\ufe52\ufe54-\ufe57\ufe5f"\
                "-\ufe61\ufe68\ufe6a\ufe6b\uff01-\uff03\uff05-\uff07"\
                "\uff0a\uff0c\uff0e\uff0f\uff1a\uff1b\uff1f\uff20"\
                "\uff3c\uff61\uff64\uff65"


# Cut
WHITESPACE = ["\n", "\t", " ", "", "\u3000"]

CUTINPUTAREAS = (
    "cut_mode",
    "segment_size",
    "overlap",
    "merge_threshold",
    "milestone"
)

# Analyze template
ANALYZEBOXES = (
    "enable_most_frequent_words",
    "enable_minimum_occurrences"
)

ANALYZEINPUTS = (
    "token_size",
    "token_type",
    "normalization_method",
    "most_frequent_words",
    "minimum_occurrences"
)

# Rolling window
RWBOXES = ("enable_milestone", "show_points", "black_and_white")
RWINPUTS = (
    "calculation_type",
    "window_type",
    "input_type",
    "search_term",
    "search_term_denominator",
    "window_size",
    "milestone"
)

# Dendrogram
HIERARCHICALINPUT = (
    "distance_metric",
    "linkage_method",
    "orientation"
)

# Consensus tree
BCTINPUT = (
    "distance_metric",
    "linkage_method",
    "cutoff",
    "iterations",
    "replace"
)

# K-Means
KMEANINPUT = (
    "clusters",
    "visualization_method",
    "initialization_method",
    "maximum_iterations",
    "different_centroids",
    "relative_tolerance"
)

# Similarity query
SIMINPUT = ("comparison_document",)

# Top words
TOPWORDINPUT = ["comparison_method"]


# Defaults
DEFAULT_SCRUB_OPTIONS = {
    "keep_apostrophes": False,
    "keep_ampersands": False,
    "remove_digits": True,
    "keep_hyphens": False,
    "make_lowercase": True,
    "remove_newlines": True,
    "remove_punctuation": True,
    "remove_tabs": True,
    "remove_spaces": True,
    "scrub_tags": False,
    "stop_words": "",
    "stop_words_method": "Off",
    "special_characters": "",
    "consolidations": "",
    "lemmas": "",
    "special_characters_preset": "None",
    "file_uploads": {
        "stop_words_file[]": "",
        "lemmas_file[]": "",
        "consolidations_file[]": "",
        "special_characters_file[]": ""}}

DEFAULT_CUT_OPTIONS = {
    "cut_mode": "Tokens",
    "segment_size": "",
    "overlap": "0",
    "merge_threshold": "50",
    "milestone": ""
}

DEFAULT_ROLLINGWINDOW_OPTIONS = {
    "enable_milestone": False,
    "show_points": False,
    "black_and_white": False,
    "calculation_type": "average",
    "window_type": "word",
    "input_type": "Words",
    "search_term": "",
    "search_term_denominator": "",
    "window_size": "",
    "milestone": ""}

DEFAULT_ANALYZE_OPTIONS = {
    "token_size": "1",
    "token_type": "Tokens",
    "normalization_method": "Proportional",
    "enable_most_frequent_words": False,
    "most_frequent_words": "100",
    "enable_minimum_occurrences": False,
    "minimum_occurrences": "1"
}

DEFAULT_HIERARCHICAL_OPTIONS = {
    "distance_metric": "euclidean",
    "linkage_method": "Average",
    "orientation": "Bottom"
}

DEFAULT_BCT_OPTIONS = {
    "distance_metric": "euclidean",
    "linkage_method": "Average",
    "cutoff": 0.5,
    "iterations": 100,
    "replace": "Without"
}

DEFAULT_KMEAN_OPTIONS = {
    "clusters": "",
    "visualization_method": "Voronoi",
    "initialization_method": "K-Means++",
    "maximum_iterations": 300,
    "different_centroids": 10,
    "relative_tolerance": 1e-4}

DEFAULT_SIM_OPTIONS = {"comparison_document": ""}

DEFAULT_TOPWORD_OPTIONS = {"comparison_method": "Each Document to the Corpus"}


# Do not cache options
SESSION_DO_NOT_CACHE = {}
WORKSPACE_DO_NOT_CACHE = {}
