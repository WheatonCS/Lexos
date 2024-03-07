let document_previews
let cut_mode
let previous_cut_mode = 'Default'

$(function () {
  // Initialize validation
  initialize_validation(validate_inputs)

  // Display the loading overlay on the "Previews" section
  start_loading('#previews')

  // Send a request for the document preview data
  $.ajax({type: 'GET', url: 'document-previews'})

  // If the request was successful, create a preview for each active
  // document
    .done(function (response) {
      document_previews = parse_json(response)
      initialize_document_previews(response)
    })

  // If the request failed, display an error and "Loading Failed" text
    .fail(function () {
      error('Failed to retrieve the document previews.')
      add_text_overlay('#previews', 'Loading Failed')
      enable('#preview-button, #apply-button')
    })

  // Perform the cutting if the "Preview" or "Apply" button is pressed
  $('#preview-button').click(function () { cut('preview') })
  $('#apply-button').click(function () { cut('apply') })

  // Load the appropriate content for the "Cut Settings" section when the
  // "Cut Mode" setting is changed
  $('#cut-mode-section input').change(load_cut_settings_section)

  // Initialize the "Tokenize", "Normalize", and "Cull" tooltips
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Loads the appropriate content for the "Cut Settings" section.
 * @returns {void}
 */
function load_cut_settings_section () {
  // Return if the same cut mode was selected
  cut_mode = $('#cut-mode-grid input:checked').val()
  if (cut_mode !== 'Segments' &&
        cut_mode !== 'Milestones') cut_mode = 'Default'
  if (cut_mode === previous_cut_mode) return

  // Hide the cut settings
  let cut_settings_grid_element = $('#cut-settings-grid')
  cut_settings_grid_element.css('opacity', '0')

  let segment_text = $('#segment-size-label')

  // If the cut mode is set to "Segments"...
  if (cut_mode === 'Segments') {
    previous_cut_mode = 'Segments'
    hide(`#milestone-input, #overlap-input, #merge-threshold-input,
            #segment-size-tooltip-button`)
    segment_text.text('Number of Segments')
    show('#segment-size-input, #number-of-segments-tooltip-button')

  // Otherwise, if the cut mode is set to "Milestones"...
  } else if (cut_mode === 'Milestones') {
    previous_cut_mode = 'Milestones'
    hide(`#segment-size-input, #overlap-input, #merge-threshold-input`)
    show('#milestone-input')

  // Otherwise, if the cut mode is set to "Tokens", "Characters", or
  // "Lines"...
  } else {
    previous_cut_mode = 'Default'
    hide('#milestone-input, #number-of-segments-tooltip-button')
    segment_text.text('Segment Size')
    show(`#segment-size-input, #overlap-input,
            #merge-threshold-input, #segment-size-tooltip-button`)
  }

  // Set the legacy "cutByMS" input if the cut mode is "milestone"
  $('#cut-by-milestone-input').val(cut_mode === 'Milestones' ? 'on' : 'off')

  // Fade in the settings
  fade_in(cut_settings_grid_element)
}

/**
 * Cuts the active documents.
 * @param {string} action The cut operation action ("preview" or "apply").
 * @returns {void}
 */
function cut (action) {
  // Validate the inputs. If the inputs are invalid, return
  if (!validate_inputs(true)) return

  // Display the loading overlay and disable the buttons on the document
  // previews section
  start_document_previews_loading()

  // Load the form data and add an entry for the cut action
  let form_data = new FormData($('form')[0])
  form_data.append('action', action)

  // Create a copy of the cut settings for each document to satisfy legacy
  // requirements
  let options = ['cut_mode', 'segment_size', 'overlap',
    'merge_threshold', 'milestone']
  for (const document of document_previews) {
    for (const option of options) { form_data.append(option + '_' + document[0], form_data.get(option)) }
  }

  // Send the cut request
  $.ajax({
    type: 'POST',
    url: 'cut/execute',
    processData: false,
    contentType: false,
    data: form_data
  })

    // If the request is successful, update the document previews with the
    // cut previews returned in the response
    .done(create_document_previews)

    // If the request failed, display an error and remove the loading overlay
    .fail(function () {
      error('Failed to cut the documents.')
      add_text_overlay('#previews', 'Loading Failed')
      enable('#preview-button, #apply-button')
    })
}

/**
 * Creates the document previews.
 * @param {string} response The response containing the new previews.
 * @returns {void}
 */
function create_document_previews (response) {
  let previews = parse_json(response)

  // If there are no previews, display "No Previews" text
  if (!previews.length) add_text_overlay('#previews', 'No Previews')

  // Otherwise, create the previews
  else {
    for (const preview of previews) { create_document_preview(preview[2], preview[3]) }
  }

  // Remove the loading overlay, fade in the previews, and enable the
  // buttons for the document previews section
  finish_document_previews_loading()

  // Update the active document count
  update_active_document_count()
}

/**
 * Validate the inputs.
 * @param {boolean} show_error Whether to show an error on invalid input.
 * @returns {boolean} Whether the inputs are valid.
 */
function validate_inputs (show_error = false) {
  // Remove any existing errors and error highlights
  remove_highlights()
  if (show_error) remove_errors()

  // "Milestone"
  let valid = true
  if (cut_mode === 'Milestones') {
    if ($('#milestone-input input').val().length <= 0) {
      error_highlight('#milestone-input input')
      if (show_error) error('A milestone must be provided.')
      valid = false
    }
    return true
  }

  // "Segment size"
  let segment_size = $('#segment-size-input input').val()
  let int_segment_size = parseInt(segment_size)
  if (!validate_number(segment_size, 1)) {
    error_highlight('#segment-size-input input')
    if (show_error) error('Invalid segment size.')
    valid = false
  }

  // "Segments"
  if (cut_mode === 'Segments') return true

  // "Overlap"
  let overlap = $('#overlap-input input').val()
  let int_overlap = parseInt(overlap)
  if (!validate_number(overlap, 0)) {
    error_highlight('#overlap-input input')
    if (show_error) error('Invalid overlap size.')
    valid = false
  }

  if (int_overlap >= int_segment_size) {
    error_highlight('#overlap-input input')
    if (show_error) {
      error(`The overlap cannot be greater than or equal to
            the segment size.`)
    }
    valid = false
  }

  // "Merge threshold"
  if (!validate_number($('#merge-threshold-input input').val(), 0, 100)) {
    error_highlight('#merge-threshold-input input')
    if (show_error) error('Invalid merge threshold.')
    valid = false
  }

  return valid
}

/**
 * Initialize the tooltips.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Cut Mode"
  create_tooltip('#cut-mode-tooltip-button', `Lexos uses spaces between
    tokens to determine where to cut documents into the specified number,
    so this tool may not work if you used Scrubber to strip white spaces
    from your documents.`)

  // "Segment Size"
  create_tooltip('#segment-size-tooltip-button', `A positive integer used to
    divide up the text. Either the number of letters, words, or lines
    per segment.`)

  // "Number of Segments"
  create_tooltip('#number-of-segments-tooltip-button', `The number of
    segments per document.`)

  // "Overlap"
  create_tooltip('#overlap-tooltip-button', `The amount of overlapping
    content at the start and end of segments. This number must be smaller
    than the segment size.`, true)

  // "Merge %"
  create_tooltip('#merge-threshold-tooltip-button', `The size of the last
    segment must be at least as large as the given percentage relative to
    other segment sizes. If the length of the last segment is below this
    threshold, it will be attached to the previous segment.`, true)

  // "Milestone"
  create_tooltip('#milestone-tooltip-button', `Split the document into
    segments at each appearance of the provided string. Child segments will not
    contain the Milestone delimiter.`)
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to the Cut page!`,
      position: 'top'
    },
    {
      element: '#cut-mode-section',
      intro: `This is the Cut Mode section. Here you can specify how you
        would like to cut up your documents.`,
      position: 'top'
    },
    {
      element: '#cut-settings-section',
      intro: `Based on your selection in the Cut Mode section, there are
        additional settings to fill out before you can initiate a
        cut.`,
      position: 'top'
    },
    {
      element: '#preview-button',
      intro: `Similar to Scrub, you can preview your changes without
                saving them here.`,
      position: 'top'
    },
    {
      element: '#apply-button',
      intro: `Unlike in Scrub, Apply works by creating new documents
        based on your cutting parameters. The original document is
        kept intact, but is deselected.`,
      position: 'top'
    },
    {
      element: '#help-button',
      intro: `For a more in-depth look at this page, visit the Help section.`,
      position: 'bottom'
    },
    {
      element: '#navbar-right',
      intro: `Once you're satisfied with your cut documents, you can
        move on to other pages in Prepare, Visualize, or Analyze.`,
      position: 'bottom'
    },
    {
      intro: `This concludes the Cut walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
