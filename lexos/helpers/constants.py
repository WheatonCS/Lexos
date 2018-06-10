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
    '~\AppData\Local\Temp') if os.name == 'nt' else '/tmp/'
UPLOAD_FOLDER = os.path.join(TMP_FOLDER, 'Lexos_' + str(getpass.getuser()))
CACHE_FOLDER = os.path.join(UPLOAD_FOLDER, 'cache/')
RESOURCE_DIR = "resources/"

'''file name'''
FILEMANAGER_FILENAME = 'filemanager.p'
SESSION_FILENAME = 'session.p'
DENDROGRAM_NEWICK_FILENAME = 'newNewickStr.txt'
FILE_INFORMATION_FIGNAME = 'statistic.svg'
CORPUS_INFORMATION_FIGNAME = 'corpus_statistic.svg'
WORKSPACE_FILENAME = 'workspace.lexos'
PCA_SMALL_GRAPH_FILENAME = 'small_PCA.html'
PCA_BIG_GRAPH_FILENAME = 'big_PCA.html'
KMEANS_GRAPH_FILENAME = 'kmeans.svg'
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
DENDRO_TITLE_FONT_SIZE = 15
DENDRO_LEGEND_FONT_SIZE = 10
DENDRO_LEGEND_X = 0
DENDRO_LEGEND_Y = 1.05
DENDRO_CHARACTERS_PER_LINE_IN_TITLE = 80
DENDRO_MAX_LINES_PER_PAGE = 80
DENDRO_MAX_LABELS_LENGTH = 15

'''secret key <not functional for now>'''
FILEMANAGER_KEY = ''  # the key you use to encrypt your file manager
SESSION_KEY = ''  # the key you use to encrypt your session
FILE_CONTENT_KEY = ''  # the key you use to encrypt you file content

'''session caching option'''
# for general settings
GENERALSETTINGS = ('beta_onbox')

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
RWBOXES = ('rollinghasmilestone', 'hideDots', 'BWoutput')
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
HIERARCHICALBOX = ('augmented', 'dendroLegends')
HIERARCHICALINPUT = (
    'metric',
    'linkage',
    'title',
    'orientation',
    'pruning',
    'criterion')

# for kmeans Clustering
KMEANINPUT = (
    'nclusters',
    'max_iter',
    'init',
    'n_init',
    'tolerance',
    'KMeans_metric',
    'viz')
# for similarity query
SIMINPUT = ('uploadname',)
SIMBOX = ('simsuniquetokens',)

# for topword
TOPWORDINPUT = (
    'testInput',
    'groupOptionType',
    'outlierMethodType',
    "outlierTypeStd",
    "outlierTypeIQR",
    'lowerboundPC',
    'upperboundPC',
    'lowerboundRC',
    'upperboundRC',
    'useFreq')

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

DEFAULT_CSV_OPTIONS = {
    'csvdata': 'count', 'csvorientation': 'filecolumn', 'csvdelimiter': 'comma'
}

DEFAULT_ROLLINGWINDOW_OPTIONS = {
    'rollinghasmilestone': False,
    'hideDots': False,
    'BWoutput': False,
    'filetorollinganalyze': '',
    'counttype': 'average',
    'windowtype': 'letter',
    'inputtype': 'string',
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
    'title': '',
    'orientation': 'bottom',
    'pruning': '',
    'augmented': True,
    'criterion': 'maxclust',
    'threshold': '',
    'dendroLegends': False,
    'degenerated': False}

DEFAULT_KMEAN_OPTIONS = {
    'nclusters': '',
    'max_iter': '',
    'init': 'k-means++',
    'n_init': '',
    'tolerance': '',
    'KMeans_metric': '',
    'viz': 'Voronoi'}

DEFAULT_SIM_OPTIONS = {'uploadname': '', 'simsuniquetokens': True}

DEFAULT_TOPWORD_OPTIONS = {
    'testInput': 'classToPara',
    'groupOptionType': 'all',
    'outlierMethodType': 'stdErr',
    "outlierTypeStd": 'top',
    "outlierTypeIQR": 'top',
    'lowerboundPC': '0',
    'upperboundPC': '1',
    'lowerboundRC': '0',
    'upperboundRC': '0',
    'useFreq': 'PC'}

DEFAULT_XMLHANDLING_OPTION = {'Remove Tag Only': 'foo'}

'''do not cache options'''
SESSION_DO_NOT_CACHE = {}
WORKSPACE_DO_NOT_CACHE = {}
