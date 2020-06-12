/**
 * Initialize the "Tokenize", "Normalize", and "Cull" tooltips.
 * @returns {void}
 */
function initialize_analyze_tooltips () {
  // "Tokenize"
  create_tooltip('#tokenize-tooltip-button', `Divide the text into n-grams
    (by tokens or characters) of the desired length.`)

  // "Normalize"
  create_tooltip('#normalize-tooltip-button', `Set how terms are counted.
    Terms can be counted by raw (absolute) counts, by proportional
    frequencies (to account for document length), or by TF-IDF weighted
    counts.`)

  // "TF-IDF"
  create_tooltip('#tf-idf-tooltip-button', `Normalize the data for different
    document lengths using <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf"
    target="_blank">Term Frequency-Inverse Document Frequency</a>.
    Lexos uses base e (natural log) as the default.`)

  initialize_cull_tooltips()
}

/**
 * Initializes the tooltips for the "Cull" section
 * @param {boolean} on_right_edge Whether the "Cull" section is on the right edge.
 * @returns {void}
 */
function initialize_cull_tooltips (on_right_edge = true) {
  // "Cull"
  create_tooltip('#cull-tooltip-button', `Place statistical bounds on the
    terms in the document-term matrix.`, on_right_edge)

  // "Use the top X Words"
  create_tooltip('#most-frequent-words-tooltip-button', `Use only the most
    frequently occurring terms in the document-term matrix.`, on_right_edge)

  // "Must be in X documents"
  create_tooltip('#minimum-occurrences-tooltip-button', `Set the minimum
    number of documents in which terms must occur to be included in the
    document-term matrix.`, on_right_edge)
}

/**
 * Validates the inputs on the "Tokenize" and "Cull" sections.
 * @param {boolean} show_error Whether to show an error on invalid input.
 * @param {boolean} remove_existing_errors Whether to remove existing errors.
 * @returns {boolean} Whether the inputs are valid.
 */
function validate_analyze_inputs (show_error, remove_existing_errors = true) {
  // Remove any existing errors and error highlights
  if (remove_existing_errors) {
    remove_highlights()
    if (show_error) remove_errors()
  }

  // "Tokenize" - "Grams"
  let valid = true
  let grams = $('#grams-input').val()

  if (!validate_number(grams, 1)) {
    error_highlight('#grams-input')
    if (show_error) error('Invalid gram size.')
    valid = false
  }

  // "Cull" - "Use the top X terms"
  let most_frequent_words = $('#most-frequent-words-input').val()

  if ($('#most-frequent-words-checkbox').is(':checked') &&
    !validate_number(most_frequent_words, 1)) {
    error_highlight('#most-frequent-words-input')
    if (show_error) error('Invalid number of top terms.')
    valid = false
  }

  // "Cull" - "Must be in X documents"
  let minimum_documents = $('#minimum-occurrences-input').val()
  if ($('#minimum-occurrences-checkbox').is(':checked') &&
    !validate_number(minimum_documents, 1, active_document_count)) {
    error_highlight('#minimum-occurrences-input')
    if (show_error) error('Invalid number of minimum occurrences.')
    valid = false
  }

  return valid
}
