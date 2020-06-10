let csv

$(function () {
  // Initialize validation
  initialize_validation(validate_inputs)

  // Display the loading overlay on the "K-Means" section
  start_loading('#graph-container')

  // Check that there are at least two active documents, initialize the
  // legacy inputs and the "Generate" and download buttons, create the
  // k-means graph, and get the CSV data
  get_active_file_ids(initialize, '#graph-container')

  // Initialize the tooltips
  initialize_analyze_tooltips()
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Checks that there are at least two active documents, initializes the
 *   "Generate" and download buttons, creates the k-means graph, and gets the
 *   CSV data.
 * @returns {void}
 */
function initialize () {
  // If there are fewer than two active documents, display warning text
  // and return
  if (active_document_count < 2) {
    add_text_overlay('#graph-container',
      'This Tool Requires at Least Two Active Documents')
    return
  }

  // Otherwise, set the default "Clusters" value
  $('#clusters-input').val(Math.floor(active_document_count / 2) + 1)

  // Create the k-means graph and get the CSV data
  send_k_means_result_request()

  // If the "Generate" button is pressed, recreate the k-means graph
  $('#generate-button').click(function () {
    // Validate the inputs
    if (!validate_inputs(true)) return

    // Remove any existing Plotly graphs
    remove_graphs()

    // Remove any existing error messages
    remove_errors()

    // Display the loading overlays and disable the graph buttons.
    start_loading('#graph-container', '#generate-button, #png-button, ' +
        '#svg-button, #csv-button, #fullscreen-button')

    // Create the k-means graph and get the CSV data
    send_k_means_result_request()
  })

  // If the "CSV" button is pressed, download the CSV
  $('#csv-button').click(function () { download(csv, 'k-means.csv') })

  // If the "PNG" or "SVG" buttons were pressed, download the graph
  initialize_graph_download_buttons()

  // If the "Fullscreen" button is pressed, make the graph fullscreen.
  initialize_graph_fullscreen_button()
}

/**
 * Creates the k-means graph and gets the CSV data.
 * @returns {void}
 */
function send_k_means_result_request () {
  // Send a request for the k-means results
  send_ajax_form_request('/k-means/results',
    {text_color: get_color('--text-color')})

  // If the request was successful, initialize the graph, store the CSV
  // data, and enable the "Generate" and download buttons
    .done(function (response) {
      csv = response.csv
      initialize_graph(response.graph)
      enable('#generate-button, #png-button, #svg-button, #csv-button')
    })

  // If the request failed, display an error and enable the "Generate"
  // button
    .fail(function () {
      error('Failed to retrieve the k-means data.')
      add_text_overlay('#graph-container', 'Loading Failed')
      enable('#generate-button')
    })
}

/**
 * Validates the inputs in the "Options" and "Advanced" sections.
 * @param {boolean} show_error Whether to show an error on invalid input.
 * @returns {boolean} Whether the inputs are valid.
 */
function validate_inputs (show_error = false) {
  // Remove any existing errors and error highlights
  remove_highlights()
  if (show_error) remove_errors()

  // "Clusters"
  let valid = true
  if (!validate_number($('#clusters-input').val(), 1, active_document_count)) {
    error_highlight('#clusters-input')
    if (show_error) error('Invalid number of clusters.')
    valid = false
  }

  // "Maximum Iterations"
  if (!validate_number($('#maximum-iterations-input').val(), 1)) {
    error_highlight('#maximum-iterations-input')
    if (show_error) error('Invalid number of maximum iterations.')
    valid = false
  }

  // "Different Centroids"
  if (!validate_number($('#different-centroids-input').val(), 1)) {
    error_highlight('#different-centroids-input')
    if (show_error) error('Invalid number of different centroids.')
    valid = false
  }

  // "Relative Tolerance"
  if (!validate_number($('#relative-tolerance-input').val(), 0)) {
    error_highlight('#relative-tolerance-input')
    if (show_error) error('Invalid relative tolerance.')
    valid = false
  }

  if (!validate_analyze_inputs(show_error, false)) valid = false
  return valid
}

/**
 * Initialize the tooltips.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Clusters"
  create_tooltip('#clusters-tooltip-button', `The number of clusters (or
    the number of centroids). The number of clusters should always be
    fewer or equal to the number of active documents. By default, this
    value is set to half the number of active documents.`)

  // Visualization
  create_tooltip('#visualization-method-tooltip-button', `2D-Scatter plot
    and Voroni diagram will reduce the DTM to a two dimensional matrix,
    whereas 3D-Scatter plot will reduce the DTM to a three dimensional
    matrix. Compared to the scatter plots, Voronoi displays the centroids
    and draws polygons for each document cluster.`)

  // Initialization method
  create_tooltip('#initialization-method-tooltip-button', `"K-Means++
    selects initial cluster centers using a weighted probability
    distribution to speed up convergence. "Random" chooses k observations
    at random from the data to serve as the initial centroids.`)

  // "Different Centroids"
  create_tooltip('#different-centroids-tooltip-button', `The number of times
    (n) the k-means algorithm will be run with different centroid seeds.
    The final results will be the best output of those n consecutive
    runs.`)

  // "Relative Tolerance"
  create_tooltip('#relative-tolerance-tooltip-button', `Decimal, relative
        tolerance with respect to inertia to declare convergence.`)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to K-Means!`,
      position: 'top'
    },
    {
      element: '#k-means-options-section',
      intro: `These settings control how the K-Means graph will appear.
        You can set the number of clusters and the graph's type.`,
      position: 'top'
    },
    {
      element: '#advanced-options-section',
      intro: `The advanced settings control the process that the data
        goes through when generating the K-Means graph.`,
      position: 'top'
    },
    {
      element: '#tokenize-section',
      intro: `Tokenize determines how terms are counted when generating
                data.`,
      position: 'top'
    },
    {
      element: '#normalize-section',
      intro: `Normalize determines if and how term totals are weighted.`,
      position: 'top'
    },
    {
      element: '#cull-section',
      intro: `Cull limits the number of terms used to generate data, and
        is optional.`,
      position: 'top'
    },
    {
      element: '#k-means-buttons',
      intro: `Here you can generate a new K-Means. You can also choose
        to download the K-Means as a static PNG or a vector SVG.
        K-Means data is also available as a CSV file.`,
      position: 'top'
    },
    {
      intro: `This concludes the K-Means walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
