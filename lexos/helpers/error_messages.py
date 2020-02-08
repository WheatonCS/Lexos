# ----------------------Cutter Model Error Messages---------------------------
NEG_OVERLAP_LAST_PROP_MESSAGE = \
    "the overlap or last segment proportion should not be negative"
LARGER_SEG_SIZE_MESSAGE = \
    "the segment size should be larger than the overlap size"
INVALID_CUTTING_TYPE_MESSAGE = "the cutting type should be letters, lines, " \
    "number, words or milestone"
EMPTY_MILESTONE_MESSAGE = "the milestone should not be empty"
# ----------------------------------------------------------------------------


# ----------------------Similarity Model Error Messages-----------------------
NON_NEGATIVE_INDEX_MESSAGE = "the index should be larger than or equal to zero"
# ----------------------------------------------------------------------------


# ----------------------Topword Model Error Messages--------------------------
NOT_ENOUGH_CLASSES_MESSAGE = "Only one class given, cannot do Z-test by " \
                             "class, at least 2 classes needed."
# ----------------------------------------------------------------------------


# ----------------------Rolling Window Analyzer Error Messages----------------
WINDOW_SIZE_LARGE_MESSAGE = "The window size must be less than or equal to" \
                            " the length of the given document"
WINDOW_NON_POSITIVE_MESSAGE = "The window size must be a positive integer"
# ----------------------------------------------------------------------------


# ----------------------Scrubber Error Messages-------------------------------
NOT_ONE_REPLACEMENT_COLON_MESSAGE = "Invalid number of colons or commas."
REPLACEMENT_RIGHT_OPERAND_MESSAGE = \
    "Too many values on right side of replacement string."
REPLACEMENT_NO_LEFT_HAND_MESSAGE = \
    "Missing value on the left side of replacement string."
# ----------------------------------------------------------------------------


# ======================== General Errors ====================================
SEG_NON_POSITIVE_MESSAGE = "The segment size must be a positive integer."
EMPTY_DTM_MESSAGE = "Empty DTM received, please upload files."
EMPTY_LIST_MESSAGE = "The list should not be empty."
EMPTY_NP_ARRAY_MESSAGE = "The input numpy array should not be empty."

# ======================== Base Model Errors =================================
NO_DATA_SENT_ERROR_MESSAGE = 'Front end did not send data to backend'
