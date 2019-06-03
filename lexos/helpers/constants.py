import getpass
import os

""" Constants """

'''configurations'''
IS_SERVER = False
DUMPING = True

'''file dir'''
FILE_CONTENTS_FOLDER = 'filecontents/'
RESULTS_FOLDER = 'analysis_results/'
WORKSPACE_DIR = 'workspace/'
# handle the temp dir in windows
TMP_FOLDER = os.path.expanduser(
    '~\\AppData\\Local\\Temp') if os.name == 'nt' else '/tmp/'
UPLOAD_FOLDER = os.path.join(TMP_FOLDER, 'Lexos_' + str(getpass.getuser()))
CACHE_FOLDER = os.path.join(UPLOAD_FOLDER, 'cache/')
RESOURCE_DIR = "resources/"

'''file name'''
FILEMANAGER_FILENAME = 'filemanager.p'
SESSION_FILENAME = 'session.p'
FILE_INFORMATION_FIGNAME = 'statistic.svg'
CORPUS_INFORMATION_FIGNAME = 'corpus_statistic.svg'
WORKSPACE_FILENAME = 'workspace.lexos'
MALLET_INPUT_FILE_NAME = 'topicfile'
MALLET_OUTPUT_FILE_NAME = 'topicfile_for_json'
TOPWORD_CSV_FILE_NAME = 'topwordResult.csv'
DEBUG_LOG_FILE_NAME = 'debug.log'
MUFI_3_FILENAME = 'MUFI_3_DICT.tsv'
MUFI_4_FILENAME = 'MUFI_4_DICT.tsv'
STOPWORD_FILENAME = 'stopwords.p'
LEMMA_FILENAME = 'lemmas.p'
CONSOLIDATION_FILENAME = 'consolidations.p'
SPECIAL_CHAR_FILENAME = 'specialchars.p'
DIGIT_MAP_FILENAME = 'digitmap.p'
PUNCTUATION_MAP_FILENAME = 'punctuationmap.p'
AMPERSAND_FILENAME = 'ampersand.p'
HYPHEN_FILENAME = 'hyphen.p'

'''constant numbers'''
MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB
MAX_FILE_SIZE_INT = 250
MAX_FILE_SIZE_UNITS = "M"
# note: number of characters in a preview screen (e.g., on Select page)
PREVIEW_SIZE = 500
# minimum number of characters used to detect a file's encoding scheme
# upon upload
MIN_ENCODING_DETECT = 10000
MIN_NEWLINE_DETECT = 1000
CHARACTERS_PER_LINE_IN_LEGEND = 100
ROUND_DIGIT = 4

'''secret key <not functional for now>'''
FILEMANAGER_KEY = ''  # the key you use to encrypt your file manager
SESSION_KEY = ''  # the key you use to encrypt your session
FILE_CONTENT_KEY = ''  # the key you use to encrypt you file content

'''session caching option'''
# for general settings
GENERALSETTINGS = 'beta_onbox'

# for scrub
SCRUBBOXES = (
    'ampersandbox',
    'aposbox',
    'digitsbox',
    'hyphensbox',
    'lowercasebox',
    'newlinesbox',
    'punctuationbox',
    'spacesbox',
    'tabsbox',
    'tagbox',
    'whitespacebox',
    'sw_option',
)
SCRUBINPUTS = (
    'manualstopwords',
    'manualspecialchars',
    'manualconsolidations',
    'manuallemmas')
OPTUPLOADNAMES = (
    'swfileselect[]',
    'lemfileselect[]',
    'consfileselect[]',
    'scfileselect[]')
# all unicode punctuation, excluding the apostrophe char
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

# for xml handling

# for cut
WHITESPACE = ['\n', '\t', ' ', '', '\u3000']

CUTINPUTAREAS = (
    'cut_type',
    'lastprop',
    'overlap',
    'cutting_value',
    'cutsetnaming')

# for base analyze
ANALYZEBOXES = ('mfwcheckbox', 'cullcheckbox', 'greyword', 'inWordsOnly')
ANALYZEINPUTS = (
    'tokenSize',
    'tokenType',
    'normalizeType',
    'norm',
    'mfwnumber',
    'cullnumber')

# for rolling window
# if there is no comma in the end, python recognize this var as a string
# instead of a tuple
RWBOXES = ('rollinghasmilestone', 'showDots', 'BWoutput')
RWINPUTS = (
    'filetorollinganalyze',
    'counttype',
    'windowtype',
    'inputtype',
    'rollingsearchword',
    'rollingsearchwordopt',
    'rollingwindowsize',
    'rollingmilestonetype')

# for word cloud and multicloud and bubbleviz
# if there is no comma in the end, python recognize this var as a string
# instead of a tuple
CLOUDLIST = ('segmentlist',)

# for word cloud
# for multicloud
MULTICLOUDINPUTS = ('analysistype',)
MULTICLOUDFILES = ('optuploadname',)

# for BubbleViz
BUBBLEVIZBOX = ('vizmaxwords',)
BUBBLEVIZINPUT = ('minlength', 'graphsize', 'maxwords')

# for hierarchical Clustering
HIERARCHICALINPUT = (
    'metric',
    'linkage',
    'orientation'
)

# for BCT analysis
BCTINPUT = (
    'metric',
    'linkage',
    'cutoff',
    'iterations',
    'replace'
)

# for kmeans Clustering
KMEANINPUT = (
    'viz',
    'init',
    'n_init',
    'max_iter',
    'nclusters',
    'tolerance'
)

# for similarity query
SIMINPUT = ('uploadname',)
SIMBOX = ('simsuniquetokens',)

# for topword
TOPWORDINPUT = ['testInput']

'''the request form default value'''
DEFAULT_GENERALSETTINGS_OPTIONS = {'beta_onbox': False}

DEFAULT_SCRUB_OPTIONS = {
    'aposbox': False,
    'ampersandbox': False,
    'digitsbox': True,
    'hyphensbox': False,
    'lowercasebox': True,
    'newlinesbox': True,
    'punctuationbox': True,
    'tabsbox': True,
    'spacesbox': True,
    'whitespacebox': False,
    'tagbox': False,
    'manualstopwords': '',
    'sw_option': 'off',
    'manualspecialchars': '',
    'manualconsolidations': '',
    'manuallemmas': '',
    'entityrules': 'default',
    'optuploadnames': {
        'swfileselect[]': '',
        'lemfileselect[]': '',
        'consfileselect[]': '',
        'scfileselect[]': ''}}

DEFAULT_CUT_OPTIONS = {
    'cutType': 'words', 'cutValue': '', 'cutOverlap': '0', 'cutLastProp': '50'
}

DEFAULT_ROLLINGWINDOW_OPTIONS = {
    'rollinghasmilestone': False,
    'showDots': False,
    'BWoutput': False,
    'filetorollinganalyze': '',
    'counttype': 'average',
    'windowtype': 'word',
    'inputtype': 'word',
    'rollingsearchword': '',
    'rollingsearchwordopt': '',
    'rollingwindowsize': '',
    'rollingmilestonetype': ''}

DEFAULT_ANALYZE_OPTIONS = {
    'tokenSize': '1',
    'tokenType': 'word',
    'normalizeType': 'freq',
    'norm': 'l0',
    'mfwcheckbox': False,
    'mfwnumber': '100',
    'cullcheckbox': False,
    'cullnumber': '1',
    'greyword': False}

DEFAULT_CLOUD_OPTIONS = {'segmentlist': []}

DEFAULT_MULTICLOUD_OPTIONS = {'optuploadname': '', 'analysistype': 'userfiles'}

DEFAULT_BUBBLEVIZ_OPTIONS = {
    'minlength': '0',
    'graphsize': '800',
    'maxwords': '100'}

DEFAULT_HIERARCHICAL_OPTIONS = {
    'metric': 'euclidean',
    'linkage': 'average',
    'orientation': 'bottom'
}

DEFAULT_BCT_OPTIONS = {
    'metric': 'euclidean',
    'linkage': 'average',
    'cutoff': 0.5,
    'iterations': 100,
    'replace': 'without'
}

DEFAULT_KMEAN_OPTIONS = {
    'nclusters': '',  # This value has to be decided by number of files.
    'viz': 'Voronoi',
    'init': 'k-means++',
    'n_init': 10,
    'max_iter': 300,
    'tolerance': 1e-4}

DEFAULT_SIM_OPTIONS = {'uploadname': '', 'simsuniquetokens': True}

DEFAULT_TOPWORD_OPTIONS = {'testInput': 'allToPara'}

DEFAULT_XMLHANDLING_OPTION = {'Remove Tag Only': 'foo'}

'''do not cache options'''
SESSION_DO_NOT_CACHE = {}
WORKSPACE_DO_NOT_CACHE = {}

# Error codes for front end
SERVER_ERROR_400 = 400
