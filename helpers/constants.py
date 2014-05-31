""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILECONTENTS_FOLDER = 'filecontents/'
RESULTS_FOLDER = 'analysis_results/'

PREVIEW_SIZE = 50 # note: number of words

FILEMANAGER_FILENAME = 'filemanager.p'
FILELABELSFILENAME = 'filelabels.p'
SETIDENTIFIER_FILENAME = 'identifierlist.p'
DENDROGRAM_FILENAME = 'dendrogram.png'
RWADATA_FILENAME = 'rwadata.p'

SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox', 'tagbox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')
OPTUPLOADNAMES = ('swfileselect[]', 'lemfileselect[]', 'consfileselect[]', 'scfileselect[]')
CUTINPUTAREAS = ('cut_type', 'lastprop', 'overlap', 'cutting_value', 'cutsetnaming')
ANALYZEOPTIONS = ('orientation', 'title', 'metric', 'pruning', 'linkage')

CHARACTERS_PER_LINE_IN_LEGEND = 80