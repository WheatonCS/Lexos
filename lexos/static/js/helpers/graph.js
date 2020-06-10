/**
 * Creates a Plotly graph.
 * @param {string} url The URL to send the request for the Plotly graph to.
 * @param {function} callback The function to call when loading completes.
 *      By default, the function re-enables the "Generate" button.
 * @returns {void}
 */
function create_graph (url, callback =
function () { enable('#generate-button') }) {
  // Send the request for the Plotly graph
  send_ajax_form_request(url, {text_color: get_color('--text-color'),
    highlight_color: get_color('--highlight-color')})

  // Always call the callback
    .always(callback)

  // If the request was successful, initialize the graph
    .done(function (response) {
      initialize_graph(response)
    })

  // If the request failed, display an error and "Loading Failed" text
    .fail(function () {
      error('Failed to retrieve the Plotly data.')
      add_text_overlay('#graph-container', 'Loading Failed')
    })
}

/**
 * Initializes the Plotly graph.
 * @param {string} graph_html The Plotly graph HTML to display.
 * @returns {void}
 */
function initialize_graph (graph_html) {
  // Add the Plotly graph HTML
  $(`<div id="graph" class="hidden"></div>`)
    .html(graph_html)
    .appendTo('#graph-container')

  // Update the graph size
  update_graph_size()
  $(window).resize(update_graph_size)

  // Remove the loading overlay and show the graph
  finish_loading('#graph-container', '#graph',
    '#png-button, #svg-button, #fullscreen-button')
}

/**
 * Removes any existing Plotly graphs.
 * @returns {void}
 */
function remove_graphs () {
  for (const element of $('.js-plotly-plot')) Plotly.purge(element)
}

/**
 * Updates the size of the graph to fit its containing element.
 * @returns {void}
 */
function update_graph_size () {
  // Get the containing element
  let graph_container_element = $('#graph-container')

  // Resize the graph to fit the graph container
  Plotly.relayout($('.js-plotly-plot')[0], {width: graph_container_element.width(),
    height: graph_container_element.height(),
    responsive: false},
  {autosize: false})
}

/**
 * Enables the "PNG" and "SVG" Plotly graph download buttons.
 * @returns {void}
 */
function initialize_graph_download_buttons () {
  // If the "PNG" button is pressed, save the graph as a PNG
  $('#png-button').click(function () { save_graph('png') })

  // If the "SVG" button is pressed, save the graph as an SVG
  $('#svg-button').click(function () { save_graph('svg') })
}

/**
 * Save the Plotly graph.
 * @param {string} format: The format to save the graph as.
 * @returns {void}
 */
function save_graph (format) {
  let graph_container_element = $('#graph-container')
  let default_width = Math.round(graph_container_element.width())
  let default_height = Math.round(graph_container_element.height())

  // Create a popup prompting for the resolution
  let popup_container_element =
        create_ok_popup(`Save as ${format.toUpperCase()}`)

  $(`
        <div id="save-graph-popup-content">
            <div><h3>Width: </h3><input id="popup-width-input" value="${default_width}" type="text" spellcheck="false" autocomplete="off"></div>
            <div><h3>Height: </h3><input id="popup-height-input" value="${default_height}" type="text" spellcheck="false" autocomplete="off"> </div>
        </div>
    `).appendTo('.popup-content')

  // If the popup's "OK" button is pressed...
  $(popup_container_element.find('.popup-ok-button')).click(function () {
    // Validate the inputs
    let width = $(popup_container_element
      .find('#popup-width-input')).val()

    let height = $(popup_container_element
      .find('#popup-height-input')).val()

    if (!validate_number(width, 1, 4096) ||
            !validate_number(height, 1, 4096)) {
      error('Invalid resolution.')
      return
    }

    // Remove any error messages
    remove_errors()

    // Save the image and close the popup
    Plotly.toImage($('.js-plotly-plot')[0],
      {format: format, width: width, height: height})
      .then(function (data) {
        download(data, `graph.${format}`, false)
        close_popup()
      })
  })
}

/**
 * Opens the graph in fullscreen mode.
 * @returns {void}
 */
function initialize_graph_fullscreen_button () {
  $('#fullscreen-button').click(() =>
    $('#graph-container')[0].requestFullscreen())
}
