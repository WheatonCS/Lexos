let table
let elements_loaded = 0

$(function () {
  // Initialize validation
  initialize_validation(validate_analyze_inputs)

  // Display the loading overlays
  start_loading(`#graph-container, #table, #corpus-statistics,
    #standard-error-test, #interquartile-range-test`)

  // Initialize the prediction statistics table
  table = new Table('statistics', '/classifier/prediction-statistics',
    '#table-section', 'Prediction Statistics', validate_analyze_inputs,
    function () { loading_complete_check() }, true, true, false, true,
    false)

  // Create the statistics and initialize the "Generate" button.
  initialize()

  // Initialize the tooltips
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})
