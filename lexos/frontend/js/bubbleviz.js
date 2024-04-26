$(function () {
  // Initialize the "Color" button
  initialize_color_button(send_word_counts_request)

  // Create the bubbleviz
  send_word_counts_request()

  // If the "Generate" button is pressed, recreate the bubbleviz
  $('#generate-button').click(send_word_counts_request)

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Sends the request for the word counts and creates the bubbleviz.
 * @returns {void}
 */
function send_word_counts_request () {
  // Validate the "Term Count" input
  if (!validate_visualize_inputs()) return

  // Remove any existing error messages
  remove_errors()

  // Display the loading overlay and disable the "PNG", "SVG" and "Generate"
  // buttons
  start_loading('#bubbleviz', '#png-button, ' +
        '#svg-button, #generate-button, #fullscreen-button')

  // Send the request for the word counts
  $.ajax({
    type: 'POST',
    url: 'bubbleviz/get-word-counts',
    contentType: 'application/JSON',
    data: JSON.stringify({maximum_top_words: $('#term-count-input').val()})
  })

  // If the request is successful, create the bubbleviz
    .done(create_bubbleviz)

  // If the request failed, display an error message, display
  // "Loading Failed" text, and enable the "Generate" button
    .fail(function () {
      error('Failed to retrieve the bubbleviz data.')
      add_text_overlay('#bubbleviz', 'Loading Failed')
      enable('#generate-button')
    })
}

/**
 * Create the bubbleviz.
 * @param {string} response The response from the "bubbleviz/get-word-counts"
 *   request.
 * @returns {void}
 */
function create_bubbleviz (response) {
  let word_counts = parse_json(response)

  // If there are no word counts, display "No Active Documents" text and
  // return
  if (!word_counts.length) {
    add_text_overlay('#bubbleviz', 'No Active Documents')
    return
  }

  // Parse the response for the dataset of word counts
  let dataset = {children: word_counts}

  // Set the diameter of the bubbleviz graph as the minimum axis of the
  // bubbleviz element
  let bubbleviz_element = $('#bubbleviz')
  let diameter = Math.min(bubbleviz_element.width(),
    bubbleviz_element.height())

  // Create the tooltip
  let tooltip = d3.select('#bubbleviz').append('h3')
    .text('No selection')
    .attr('class', 'visualize-tooltip')

  // Create the bubbleviz
  let bubble = d3.pack(dataset)
    .size([diameter, diameter])
    .padding(3)

  let svg = d3.select('#bubbleviz')
    .append('svg')
    .attr('version', '1.1')
    .attr('xmlns', 'http://www.w3.org/2000/svg')

    .attr('width', diameter + 'px')
    .attr('height', diameter + 'px')
    .attr('class', 'bubble')

  let nodes = d3.hierarchy(dataset)
    .sum(function (d) { return d.value })

  let node = svg.selectAll('.node')
    .data(bubble(nodes).descendants())
    .enter()
    .filter(function (d) { return !d.children })
    .append('g')
    .attr('class', 'node')
    .attr('transform', function (d) {
      return 'translate(' + d.x + ', ' + d.y + ')'
    })

  // Create the bubbles
  node.append('circle')
    .attr('r', function (d) { return d.r })
    .style('fill', function (d) {
      return get_visualize_color(d.data.value)
    })

  // If the bubble is moused over, create a tooltip with information on
  // the bubble and highlight the bubble
    .style('transition', 'opacity var(--fade-duration)')
    .on('mouseover', function () {
      d3.select(this.parentNode.childNodes[0]).style('opacity', '.7')
      tooltip.style('opacity', '1')
    })
    .on('mousemove', function (d) {
      tooltip
        .html(`Word: ${d.data.word}<br/>Count: ${d.data.count}`)
        .style('left', `${d3.event.pageX + 34}px`)
        .style('top', `${d3.event.pageY - 12}px`)
    })
    .on('mouseout', function () {
      d3.select(this.parentNode.childNodes[0]).style('opacity', '1')
      tooltip.style('opacity', '0')
    })

  // Create the bubble text
  node.append('text')
    .attr('dy', '.3em')
    .style('text-anchor', 'middle')
    .text(function (d) { return d.data.word })
    .attr('font-family', $('#font-input').val())
    .attr('font-size', function (d) { return d.r / ((d.data.word.length + 1) / 3) })
    .attr('fill', 'var(--foreground-color)')
    .style('pointer-events', 'none')

  // Fade in the bubbleviz
  d3.select(self.frameElement).style('height', diameter + 'px')
  finish_loading('#bubbleviz', '#bubbleviz', '#png-button, ' +
        '#svg-button, #generate-button, #fullscreen-button')

  // Initialize the SVG and PNG download buttons
  initialize_png_link('#bubbleviz svg', '#png-button',
    diameter, diameter, 'bubbleviz.png')
  initialize_svg_link('#bubbleviz svg', '#svg-button', 'bubbleviz.svg')

  // Initialize the fullscreen button
  initialize_visualize_fullscreen_button()
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to Bubbleviz!`,
      position: 'top'
    },
    {
      element: '#visualize-font',
      intro: `You can change the font-style of your Bubbleviz here,
        provided your computer has access to the font.`,
      position: 'top'
    },
    {
      element: '#visualize-term-count',
      intro: `You can change the amount of words displayed in your
        Bubbleviz here.`,
      position: 'top'
    },
    {
      element: '#visualize-color',
      intro: `You can choose from a variety of color themes from the
        dropdown menu here. Click "OK" to generate.`,
      position: 'top'
    },
    {
      element: '#visualize-buttons',
      intro: `You can generate a new Bubbleviz at any time here. You can
        also choose to download a static PNG or vector SVG.`,
      position: 'top'
    },
    {
      intro: `This concludes the Bubbleviz walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
