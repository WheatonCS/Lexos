let csv

$(function () {
  // Initialize validation
  initialize_validation(validate_inputs)

  // Display the loading overlay
  start_loading('#graph-container')

  // If the "Calculation Type" is changed...
  $(`input[name="calculation_type"]`).change(function () {
    // If the calculation type is "Rolling Average", display hide the
    // denominator input and clear its input
    if ($(`input[name="calculation_type"]:checked`).val() === 'Rolling Average') {
      $('#search-terms-input-denominator').css('display', 'none').find('input').val('')

    // Otherwise, display the denominator input
    } else $('#search-terms-input-denominator').css('display', 'inline')
  })

  // Check that there is exactly one document active and display the
  // appropriate text on the "Rolling Window" section
  get_active_file_ids(single_active_document_check, '#graph-container')

  // Initialize the tooltips
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Checks that there is exactly one document active and sets the appropriate
 * text in the "Rolling Window" section.
 * @param {string} response The response from the "get-active-files" request.
 * @returns {void}
 */
function single_active_document_check (response) {
  // Get the active documents
  let documents = Object.entries(parse_json(response))

  // If there are no active documents, display "No Active Documents" text
  // on the "Rolling Window" section
  if (documents.length === 0) {
    add_text_overlay('#graph-container', 'No Active Documents')

  // If there is more than one active document, display "This Tool Requires
  // A Single Active Document" text on the "Rolling Window" section
  } else if (documents.length > 1) {
    add_text_overlay('#graph-container', 'This Tool Requires a Single Active Document')

  // Otherwise, set the legacy form input for the file to analyze to the
  // active document, display "No Graph" text on the "Rolling Window"
  // section, and enable the generate button
  } else {
    add_text_overlay('#graph-container', 'No Graph')
    $('#file-to-analyze').val(documents[0][0])
    enable('#generate-button')
  }

  // If the "Generate" button is clicked, create the rolling window graph
  $('#generate-button').click(create_rolling_window)

  // Initialize the "PNG" and "SVG" download buttons
  initialize_graph_download_buttons()

  // If the "CSV" button is pressed, download the CSV
  $('#csv-button').click(function () {
    download(csv, 'rolling-window.csv')
  })

  // If the "Fullscreen" button is pressed, make the graph fullscreen.
  initialize_graph_fullscreen_button()
}

/**
 * Creates the rolling window.
 * @returns {void}
 */
function create_rolling_window () {
  // Validate the inputs
  if (!validate_inputs(true)) return

  // Remove any existing Plotly graphs
  remove_graphs()

  // Remove any existing error messages
  remove_errors()

  // Display the loading overlay and disable the appropriate buttons
  start_loading('#graph-container', '#generate-button, ' +
        '#png-button, #svg-button, #csv-button, #full-screen-button')

  // Create the rolling window graph and get the CSV data
  send_rolling_window_result_request()
}

/**
 * Creates the rolling window graph and gets the CSV data.
 * @returns {void}
 */
function send_rolling_window_result_request () {
  // Send a request for the k-means results
  send_ajax_form_request('/rolling-window/results',
    {text_color: get_color('--text-color')})

  // If the request was successful, initialize the graph, store the CSV
  // data and enable the appropriate buttons
    .done(function (response) {
      csv = response.csv
      initialize_graph(response.graph)
      enable('#generate-button, #csv-button')
    })

  // If the request failed, display an error and enable the "Generate"
  // button
    .fail(function () {
      error('Failed to retrieve the rolling window data.')
      enable('#generate-button')
    })
}

/**
 * Validates the inputs.
 * @param {boolean} show_error Whether to show an error on invalid input.
 * @returns {boolean} Whether the inputs are valid.
 */
function validate_inputs (show_error = false) {
  // Remove any existing errors and error highlights
  remove_highlights()
  if (show_error) remove_errors()

  // "Search terms"
  let valid = true
  if ($('#search-terms-input input').val().length < 1) {
    error_highlight('#search-terms-input input')
    if (show_error) error('Please enter the search terms.')
    valid = false
  }

  if ($(`input[name="calculation_type"]:checked`).val() === 'Rolling Ratio' &&
    $('#search-terms-input-denominator input').val().length < 1) {
    error_highlight('#search-terms-input-denominator input')
    if (show_error) error('Please enter the search terms.')
    valid = false
  }

  // "Window"
  if (!validate_number($('#window-size-input').val(), 1)) {
    error_highlight('#window-size-input')
    if (show_error) error('Invalid window size.')
    valid = false
  }

  // "Milestone"
  if ($('#milestone-checkbox').prop('checked') &&
    $('#milestone-input').val().length < 1) {
    error_highlight('#milestone-input')
    if (show_error) {
      error(`Please either enter a milestone or uncheck the milestone option.`)
    }
    valid = false
  }

  return valid
}

/**
 * Initializes the tooltips.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Rolling Average"
  create_tooltip('#rolling-average-tooltip-button', `Measures the number of
    times the input appears in the window, divided by the overall size of
    the window.`)

  // "Rolling Ratio"
  create_tooltip('#rolling-ratio-tooltip-button', `Measures the value of the
    first input divided by the sum of the first and second inputs.`)

  // "Search Terms" input
  create_tooltip('#search-terms-input-tooltip-button', `Please divide inputs
    by commas. For rolling ratios, input the numerator and denominator.`)

  // "Strings"
  create_tooltip('#strings-tooltip-button', `A string can be of any length.
    When searching for multiple stings, separate each string by comma with
    no whitespace. Any entered whitespace will be included in the
    search.`)

  // "Regex"
  create_tooltip('#regex-tooltip-button', `Visit
    <a href="https://en.wikipedia.org/wiki/Regular_expression"
    target="_blank">this page</a> for more information on regular
    expressions.`)

  // "Window"
  create_tooltip('#window-size-tooltip-button', `The number of characters,
    tokens, or lines each window should contain. The maximum size is
    10000.`)

  // "Milestone"
  create_tooltip('#milestone-tooltip-button', `Search the file for all
    instances of a specified string and plot a vertical dividing line at
    those locations.`, true)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to Rolling Window! This tool requires both a
        single active document and a few required settings to create
        the graph.`,
      position: 'top'
    },
    {
      element: '#calculation-type-section',
      intro: `Here you can choose how the data is graphed.`,
      position: 'top'
    },
    {
      element: '#search-terms-section',
      intro: `Choose what type of search you will make and enter the
        terms here.`,
      position: 'top'
    },
    {
      element: '#window-section',
      intro: `Set the size and units to count in each window.`,
      position: 'top'
    },
    {
      element: '#display-section',
      intro: `These settings are optional. Checking any of these boxes
        will add the feature to the graph.`,
      position: 'top'
    },
    {
      element: '#rolling-window-buttons',
      intro: `Generate your graph here. You can also choose to download
        your graph as a static PNG or vector SVG. Additionally, the
        data of your graph can be downloaded as a CSV file.`,
      position: 'top'
    },
    {
      intro: `This concludes the Rolling Window walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
