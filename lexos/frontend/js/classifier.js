let table
let elements_loaded = 0

$(function () {
  // Initialize validation
  initialize_validation(validate_analyze_inputs)

  // Display the loading overlays
  start_loading(`#graph-container, #table, #prediction-statistics`)

  // Initialize the prediction statistics table
  table = new Table('statistics', '/classifier/prediction-statistics',
    '#table-section', 'Prediction Statistics', validate_analyze_inputs,
    function () { loading_complete_check() }, false, true, false, false,
    true)

  // Create the statistics and initialize the "Generate" button.
  initialize()

  // Initialize the tooltips
  initialize_tooltips()

  initialize_tree_options()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Creates the statistics and initializes the "Generate" button.
 * @returns {void}
 */
 function initialize () {
  // If there are no active documents, display "No Active Documents" text
  // and return
  if (!active_document_count) {
    add_text_overlay(`#graph-container, #table, #prediction-statistics`,
    'No Active Documents')
    return
  }

  // Otherwise, create the statistics
  //dont forget
  //create_statistics()

  // If the "Generate" button is pressed, recreate the statistics
  $('#generate-button').click(function () {
    // Validate the inputs
    if (!validate_analyze_inputs(true)) return

    // Remove any existing Plotly graphs
    remove_graphs()

    // Remove any existing error messages
    remove_errors()

    // Display the loading overlays and disable the appropriate buttons
    start_loading('#graph-container, #prediction-statistics, ' +
      '#generate-button, #png-button, #svg-button, #fullscreen-button')

    // Create the statistics
    //dont forget
    //create_statistics()
  })

  // If the "PNG" or "SVG" buttons are pressed, download the graph
  initialize_graph_download_buttons()

  // If the "Fullscreen" button is pressed, make the graph fullscreen.
  initialize_graph_fullscreen_button()
}
/**
 * Re-enables the "Generate" button if all elements have finished loading.
 * @param {number} number_loaded The number of elements that were loaded by
 *   the calling function.
 * @returns {void}
 */
 function loading_complete_check (number_loaded = 1) {
  // Increment "elements_loaded" by the number of elements loaded by the
  // calling function
  elements_loaded += number_loaded

  // If all 5 elements have not finished loading, return
  if (elements_loaded < 5) return

  // Otherwise, re-enable the "Generate" button and reset "elements_loaded"
  $('#generate-button').removeClass('disabled')
  elements_loaded = 0
}

/**
 * Initializes the tooltips for the "Tokenize" and "Cull" sections.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Tokenize"
  create_tooltip('#fit-options-tooltip-button', `Fit a new SVM model
      with the specified options.`)

  create_tooltip('#margin-softener-tooltip-button', `Set the margin
    softener for the classifier. This value controls how many data points 
    are allowed to stray over the descision boundary.`)

  create_tooltip('#kernel-type-tooltip-button', `Select a kernel
  for the model. A kernel is a translation into a new space to allow
  linear seperation of data that can't be linearly seperated in 2d
  space. 
  NOTE: Selecting a kernel other than linear will significantly
  slow down the fitting process.`)

  create_tooltip('#prediction-settings-tooltip-button', `Make predictions
  on the data with the SVM model.`)

  create_tooltip('#trial-count-tooltip-button', `The number of trials
  to run with the model. Data is randomly shuffled before each trial
  is run, so mutiple trials will give a better sense of the true
  prediction.`)
  // "Cull"
  initialize_cull_tooltips(false)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to the Classifier page!`,
      position: 'top'
    },
    {
      element: '#left-column',
      intro: `These are the settings for classifer. Fit and Predict
        can be used to control the model that is fit. Generate is used
        to create the graph and the prediction statistics.`,
      position: 'top'
    },
    {
      element: '#graph-section',
      intro: `Here the results of the predictions are shown. The 
      different points on the graph are the words used as data,
      and the line separating them is the decision boundary.
      This graph can be downloaded as a PNG or SVG.`,
      position: 'top'
    },
    {
      element: '#table-section',
      intro: `This table displays information concerning statistics
      about the different trials run. This table can be downloaded 
      as a CSV file.`,
      position: 'top'
    },
    {
      intro: `This concludes the Classifier walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
