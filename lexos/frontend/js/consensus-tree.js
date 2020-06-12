let image_data

$(function () {
  // Initialize validation
  initialize_validation(validate_inputs)

  // Display the loading overlay
  start_loading('#consensus-tree-body')

  // Register option popup creation callbacks for the "Distance Metric" and
  // "Linkage Method" buttons
  initialize_tree_options()

  // Create the consensus tree and initialize the "Generate" and "Download"
  // buttons
  initialize()

  // Initialize the tooltips
  initialize_analyze_tooltips()
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Creates the consensus tree and initializes the "Generate" and "Download"
 * buttons.
 * @returns {void}
 */
function initialize () {
  // If there are fewer than two active documents, display warning text
  // and return
  if (active_document_count < 2) {
    add_text_overlay('#consensus-tree-body', `This Tool Requires at Least Two Active Documents`)
    return
  }

  // Create the consensus tree
  create_consensus_tree()

  // When the "Generate" button is pressed, create the consensus tree
  $('#generate-button').click(create_consensus_tree)

  // When the "Download" button is pressed, download the consensus tree PNG
  $('#download-button').click(function () {
    download(image_data, 'consensus-tree.png', false)
  })
}

/**
 * Creates the consensus tree.
 * @returns {void}
 */
function create_consensus_tree () {
  // Validate the inputs
  if (!validate_inputs(true)) return

  // Display the loading overlay and disable the "Generate" and "Download"
  // buttons
  start_loading('#consensus-tree-body', '#generate-button, #download-button')

  // Remove any existing error messages
  remove_errors()

  // Send a request for the consensus tree data
  send_ajax_form_request('consensus-tree/graph',
    {text_color: get_color('--text-color')})

  // If the request was successful...
    .done(function (response) {
      image_data = `data:image/png;base64,${response}`

      // Create the consensus tree
      $(`
          <div id="consensus-tree" class="hidden">
              <img src="${image_data}" alt="Bootstrap Consensus Tree">
          </div>
      `).appendTo('#consensus-tree-body')

      // Remove the loading overlay, fade in the consensus tree,
      // and enable the "Generate" and "Download" buttons
      finish_loading('#consensus-tree-body',
        '#consensus-tree', '#generate-button, #download-button')
    })

  // If the request failed, display an error, and enable the "Generate"
  // button
    .fail(function () {
      error('Failed to retrieve the consensus tree data.')
      enable('#generate-button')
      add_text_overlay('#consensus-tree-body', 'Loading Failed')
    })
}

/**
 * Validate the consensus tree options inputs.
 * @param {boolean} show_error Whether to show an error on invalid input.
 * @returns {boolean} Whether the inputs are valid.
 */
function validate_inputs (show_error = false) {
  // Remove any existing errors and error highlights
  remove_highlights()
  if (show_error) remove_errors()

  // "Cutoff"
  let valid = true
  if (!validate_number($('#cutoff-input').val(), 0, 1)) {
    error_highlight('#cutoff-input')
    if (show_error) error('Invalid cutoff.')
    valid = false
  }

  // "Iterations"
  if (!validate_number($('#iterations-input').val(), 1)) {
    error_highlight('#iterations-input')
    if (show_error) error('Invalid number of iterations.')
    valid = false
  }

  if (!validate_analyze_inputs(show_error, false)) valid = false
  return valid
}

/**
 * Initializes the tooltips for the "Options" section.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Distance Metric"
  create_tooltip('#distance-metric-tooltip-button', `Different methods for
        measuring the distance (difference) between documents.`)

  // "Linkage Method"
  create_tooltip('#linkage-method-tooltip-button', `The method used to
        determine when documents and/or other sub-clusters should be joined
        into new clusters.`)

  // "Cutoff"
  create_tooltip('#cutoff-tooltip-button', `0.5 means a document must
        appear in a clade in at least 50% of the iterations.`)

  // "Iterations"
  create_tooltip('#iterations-tooltip-button', `For 100 iterations, 80% of
        the tokens will be chosen with or without replacement.`)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to Consensus Tree!`,
      position: 'top'
    },
    {
      element: '#consensus-tree-options-section',
      intro: `These settings control how the Consensus Tree is
        generated. Checking sample with replacement will allow the
        segments to be used by another iteration.`,
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
      element: '#consensus-tree-buttons',
      intro: `Here you can generate a new Consensus Tree. You can also
        choose to download the Consensus Tree as a static PNG.`,
      position: 'top'
    },
    {
      intro: `This concludes the Consensus Tree walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
