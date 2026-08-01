let layouts = []
let word_cloud_count
let rendered_count
let diameter

$(function () {
  // Initialize the "Color" button
  initialize_color_button(get_multicloud_data)

  // Create the multicloud
  get_multicloud_data()

  // If the "Generate" button is pressed, recreate the multicloud
  $('#generate-button').click(get_multicloud_data)

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Get the multicloud data.
 * @returns {void}
 */
function get_multicloud_data () {
  // Validate the "Term Count" input
  if (!validate_visualize_inputs()) return

  // Remove any error messages
  remove_errors()

  // Reset the rendered word cloud count
  rendered_count = 0

  // Display the loading overlay and disable the "PNG", "SVG" and "Generate"
  // buttons
  start_loading('#multicloud', '#png-button, #svg-button, #generate-button')

  // Send a request to get the word counts
  $.ajax({
    type: 'POST',
    url: 'multicloud/get-word-counts',
    contentType: 'application/JSON',
    data: JSON.stringify({maximum_top_words: $('#term-count-input').val()})
  })

  // If the request was successful, create the multicloud
    .done(create_word_cloud_layouts)

  // If the request failed, display an error message, display
  // "Loading Failed" text, and enable the "Generate" button
    .fail(function () {
      error('Failed to retrieve the multicloud data.')
      add_text_overlay('#multicloud', 'Loading Failed')
      enable('#generate-button')
    })
}

/**
 * Creates the multicloud (a word cloud for each active document).
 * @param {string} response: The response from the get-word-counts request.
 * @returns {void}
 */
function create_word_cloud_layouts (response) {
  // Parse the JSON response
  response = parse_json(response)

  // If there are no active documents, display "No Active Documents" text
  // and return
  word_cloud_count = response.length
  if (!word_cloud_count) {
    add_text_overlay('#multicloud', 'No Active Documents')
    return
  }

  // Otherwise, create a word cloud for each document
  for (let i = 0; i < word_cloud_count; ++i) {
    // Get the document's data
    let document = response[i]

    // Create the word cloud element
    $(`
        <div id="word-cloud-wrapper-${i}" class="word-cloud-wrapper">

            <div class="vertical-splitter section-top">
                <h3 class="title">${document.name}</h3>

                <div class="right-justified">
                    <a id="png-button-${i}" class="button">PNG</a>
                    <a id="svg-button-${i}" class="button">SVG</a>
                    <a id="fullscreen-button-${i}" class="button">Fullscreen</a>
                </div>
            </div>

            <div id="word-cloud-${i}" class="word-cloud"></div>
        </div>
    `).appendTo('#multicloud').find('.word-cloud')

    // Calculate the sizes
    diameter = rem_to_px(46)
    let base_size = diameter / 50
    let maximum_size = diameter / 3 - base_size

    // Create the list of the words' text and sizes
    let words = []
    for (const word of document.words) {
      words.push({
        'text': word[0],
        'count': word[1],
        'normalized_count': word[2],
        'size': word[2] * maximum_size + base_size
      })
    }

    // Create the layout
    create_word_cloud_layout(i, document.name, words, diameter)
  }
}

/**
 * Creates a word cloud layout.
 * @param {number} id: The ID of the layout.
 * @param {string} name: The name of the document.
 * @param {array} words: The top words in the document.
 * @param {number} diameter: The diameter of the word cloud.
 * @returns {void}
 */
function create_word_cloud_layout (id, name, words, diameter) {
  // Create the word cloud layout
  layouts[id] = d3.layout.cloud()
    .size([diameter, diameter])
    .words(words)
    .padding(5)
    .rotate(function () { return ~~(Math.random() * 2) * 90 })
    .font($('#font-input').val())
    .fontSize(function (d) { return d.size })
    .on('end', function (words) {
      create_word_cloud(id, name, words)
    })

  // Start the render
  layouts[id].start()
}

/**
 * Creates a word cloud.
 * @param {number} id: The ID of the layout.
 * @param {string} name: The name of the document.
 * @param {list} words: The words in the layout.
 * @returns {void}
 */
function create_word_cloud (id, name, words) {
  let layout = layouts[id]

  // Create the tooltip
  let tooltip = d3.select(`#word-cloud-${id}`).append('h3')
    .text('No selection')
    .attr('class', 'visualize-tooltip')

  // Create the word cloud
  d3.select(`#word-cloud-${id}`)

    .append('svg')
    .attr('width', layout.size()[0])
    .attr('height', layout.size()[1])

    .append('g')
    .attr('transform', 'translate(' +
                layout.size()[0] / 2 + ',' + layout.size()[1] / 2 + ')')
    .selectAll('text')
    .data(words)
    .enter()

    .append('text')
    .style('font-size', function (d) { return d.size + 'px' })
    .style('fill', function (d) {
      return get_visualize_color(d.normalized_count)
    })
    .style('font-family', layout.font())
    .attr('text-anchor', 'middle')
    .attr('transform', function (d) {
      return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')'
    })
    .text(function (d) { return d.text })

  // If the text is moused over, create a tooltip with information on
  // the bubble and highlight the bubble
    .style('transition', 'opacity var(--fade-duration)')
    .on('mouseover', function () {
      d3.select(this).style('opacity', '.7')
      tooltip.style('opacity', '1')
    })
    .on('mousemove', function (d) {
      tooltip
        .html(`Word: ${d.text}<br>Count: ${d.count}`)
        .style('left', (d3.event.pageX + 30) + 'px')
        .style('top', (d3.event.pageY - 12) + 'px')
    })
    .on('mouseout', function () {
      d3.select(this).style('opacity', '1')
      tooltip.style('opacity', '0')
    })

  // Initialize the PNG and SVG download buttons
  initialize_png_link(`#word-cloud-${id} svg`,
    `#png-button-${id}`, diameter, diameter, 'multicloud.png')
  initialize_svg_link(`#word-cloud-${id} svg`, `#svg-button-${id}`, 'multicloud.svg')

  // Initialize the fullscreen button
  initialize_visualize_fullscreen_button(`#fullscreen-button-${id}`, `#word-cloud-${id}`)

  // Remove the loading overlay and fade in the word clouds if this is the
  // last word cloud to render
  if (++rendered_count === word_cloud_count) {
    finish_loading('#multicloud', '.word-cloud-wrapper',
      '#png-button, #svg-button, #generate-button')
  }
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to the Multicloud page!`,
      position: 'top'
    },
    {
      element: '#multicloud',
      intro: `Here are Word Clouds for each respective document.`,
      position: 'top'
    },
    {
      element: '#visualize-font',
      intro: `You can change the font-style of each Word Cloud here
        provided your computer has access to the font.`,
      position: 'top'
    },
    {
      element: '#visualize-term-count',
      intro: `You can change the amount of words displayed in your
        clouds here.`,
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
      intro: `You can generate a new Multicloud at anytime here. You can
        also choose to download static PNGs or vector SVGs by clicking
        on each respective cloud"s button.`,
      position: 'top'
    },
    {
      intro: `This concludes the Multicloud walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
