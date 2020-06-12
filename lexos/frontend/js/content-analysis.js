let overview_table
let corpus_table
let files = []

$(function () {
  // If the "Upload" button is clicked...
  $('#dictionaries-section #upload-button').click(function () {
    // Click the file input element
    let file_input_element = $('#file-input')
    file_input_element.click()
  })

  // If files were selected for upload, upload the files
  $('#file-input').change(upload_files)

  // Initialize the formula section button callbacks
  initialize_button_callbacks()

  // If the "Analyze" button is pressed...
  $('#formula-section #analyze-button').click(
    send_content_analysis_request)

  // Initialize the overview and corpus tables
  overview_table = new Table('overview', '/content-analysis/analyze',
    '#overview-table-section', 'Overview', null, null, true, true,
    false, true, true)
  corpus_table = new Table('corpus', '/content-analysis/analyze',
    '#corpus-table-section', 'Corpus', null, null, true, true,
    true, true, true)

  // Initialize the tooltips
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Sends the content analysis request and creates the tables.
 * @returns {void}
 */
function send_content_analysis_request () {
  // Display the loading overlays and disable the "Upload" and "Analyze"
  // buttons
  start_loading('#overview-table-content, #corpus-table-content,' +
    '#documents-body', `#formula-section #analyze-button,
    #dictionaries-section #upload-button, #corpus-download-button`)

  // Remove any existing error messages
  remove_errors()

  // Send a request to analyze the files
  send_ajax_form_request('/content-analysis/analyze')

    // If the request was successful, display the results
    .done(display_results)

    // If the request failed, display an error message and remove the
    // loading overlay
    .fail(function () {
      error('Failed to perform the analysis.')
      show(`#formula-section #analyze-button,
        #dictionaries-section #upload-button`)
      add_text_overlay(`#overview-table-content, #corpus-table-content,
        #documents-body`, 'Loading Failed')
    })
}

/**
 * Initialize the formula section button callbacks.
 * @returns {void}
 */
function initialize_button_callbacks () {
  let formula_element = $('#formula-textarea')

  // If a number pad or operations pad button is clicked, add the
  // appropriate text
  $('#number-pad h3, #operations-pad h3').each(function () {
    $(this).click(function () {
      let text = $(this).text()
      let formula = formula_element.val()

      // If the "DEL" button was pressed...
      if (text === 'DEL') {
        // If the deleted character is the end of a document label,
        // delete the entire document label
        let last_character = formula.slice(-1)
        if (last_character === ']') {
          formula = formula.slice(0, formula.lastIndexOf('['))

        // Otherwise, delete a single character
        } else formula = formula.slice(0, -1)

      // If the "CLR" button was pressed, clear the formula
      } else if (text === 'CLR') formula = ''

      // If the "X" or "^" button was pressed, append the appropriate
      // text
      else if (text === 'X') formula += '*'
      else if (text === '^') formula += '^('

      // Otherwise, append the text shown on the button
      else formula += text

      formula_element.val(formula)
    })
  })

  $(`input[type="radio"][name="sort_ascending"]`).change(function () {
    send_content_analysis_request()
  })
}

/**
 * Upload files.
 * @param {event} event The event that triggered the callback.
 * @returns {void}
 */
function upload_files () {
  // Remove any existing error messages
  remove_errors()

  // Display the loading overlay
  start_loading('.dictionaries-wrapper',
    '#dictionaries-section #upload-button')

  // Send a request to upload the files
  return $.ajax({
    type: 'POST',
    url: '/content-analysis/upload-dictionaries',
    processData: false,
    contentType: false,
    data: new FormData($('form')[0])
  })

  // If the request is successful, create the upload previews
    .done(create_upload_previews)

  // If the request failed, display an error
    .fail(function () { error('Upload failed.') })
}

/**
 * Create the upload previews.
 * @param {string} response The response from the
 *   "/content-analysis/upload-dictionaries" request.
 * @returns {void}
 */
function create_upload_previews (response) {
  // Create the upload previews
  $(`<div class="hidden dictionaries"></div>`)
    .appendTo('.dictionaries-wrapper')

  for (const upload of response) { $(`<h3>${upload}</h3>`).appendTo('.dictionaries') }

  // Create the callbacks for the formula section document buttons
  let formula_element = $('#formula-textarea')
  $('#documents-pad h3:not(.centerer)').each(function () {
    $(this).click(function () {
      formula_element.val(formula_element.val() + `[${$(this).text()}]`)
    })
  })

  // Remove the loading overlay, show the dictionary buttons, and
  // enable the "Upload" button
  finish_loading('.dictionaries-wrapper', '.dictionaries',
    '#dictionaries-section #upload-button')
}

/**
 * Displays the results.
 * @param {string} response The response from the
 *   "/content-analysis/analyze" request.
 * @returns {void}
 */
function display_results (response) {
  // Check for errors
  let error_message = response['error']
  if (error_message) {
    error(error_message)
    finish_loading('#results-container', '', `#formula-section
            #analyze-button, #dictionaries-section #upload-button`)
    return
  }

  // Create the overview table
  overview_table.csv = response['overview-table-csv']
  overview_table.display(response['overview-table-body'],
    response['overview-table-head'])

  // Create the corpus table
  corpus_table.csv = response['corpus-table-csv']
  corpus_table.display(response['corpus-table-body'],
    response['corpus-table-head'])

  // Create the document tables
  $(`<div id="document-tables-grid"></div>`).appendTo('#documents-body')

  for (const document of response['documents']) {
    Table.create_basic_table('#document-tables-grid',
      document['data'], ['Dictionary', 'Phrase', 'Count'],
      document['name'], document['csv'])
  }

  // Remove the loading overlays and enable the buttons
  finish_loading('#documents-body', `#document-tables-grid .lexos-table`,
    `#formula-section #analyze-button,
        #dictionaries-section #upload-button`)
}

/**
 * Initialize the tooltips.
 * @returns {void}
 */
function initialize_tooltips () {
  create_tooltip('#dictionaries-tooltip-button', `Upload a text file
    containing a comma-separated list of key words and phrases associated
    with the characteristic to test. For example, if one is analyzing
    sentiment, a positive file might include: "happy, very happy, great,
    good".`)

  create_tooltip('#formula-tooltip-button', `Create a formula that uses the
    dictionaries to compute a final score. For example: "[happy] –
    [sad]".`, true)

  create_tooltip('#corpus-table-tooltip-button', `The top 100 words are displayed.
    For a list of all of the words, click the "Download" button.`, true)

  create_tooltip('#documents-tooltip-button', `The top 100 words are
    displayed for each document. For a list of all of the words, click
    the "Download" button.`, true)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to Content Analysis!`,
      position: 'top'
    },
    {
      element: '#dictionaries-section',
      intro: `Here you can upload dictionaries for your analysis.`,
      position: 'top'
    },
    {
      element: '#formula-section',
      intro: `Here you can create your formula using the calculator
                buttons. Buttons for each uploaded dictionary will appear on
                the right.`,
      position: 'top'
    },
    {
      element: '#formula-section #analyze-button',
      intro: `Click here to generate your data. This will take some
                time.`,
      position: 'top'
    },
    {
      element: '#overview-table-section',
      intro: `This section provides a general overview of your data.
                You can download this data as a CSV file.`,
      position: 'top'
    },
    {
      element: '#corpus-table-section',
      intro: `This section displays the most commonly used words along
                with the dictionary each word belongs to. You can download
                this data as a CSV file.`,
      position: 'top'
    },
    {
      element: '#documents-section',
      intro: `Much like the previous section, although this section
                contains the data for each individual document rather than
                the full corpus.`,
      position: 'top'
    },
    {
      intro: `This concludes the Content Analysis walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
