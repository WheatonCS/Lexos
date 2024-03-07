$(function () {
  // Display the loading overlay on the "Previews" section
  start_loading('#previews')

  // Create a preview for each active document
  $.ajax({type: 'GET', url: 'document-previews'})

  // If the request was successful, initialize the document previews
    .done(function (response) { initialize_document_previews(response) })

  // If the request failed, display an error
    .fail(function () {
      error('Failed to retrieve the document previews.')
      add_text_overlay('#previews', 'Loading Failed')
      enable('#preview-button, #apply-button')
    })

  // Disable the punctuation options when the "Remove Punctuation" checkbox
  // is unchecked
  let punctuation_checkbox_element = $('#punctuation-checkbox')
  punctuation_checkbox_element.click(function () {
    let punctuation_options_element = $('#punctuation-options')
    if (punctuation_checkbox_element.is(':checked')) { punctuation_options_element.removeClass('disabled') } else punctuation_options_element.addClass('disabled')
  })
  let tags_checkbox_element = $('#scrub-tags-checkbox')
  tags_checkbox_element.click(function () {
    let tags_options_element = $('#scrub-tags-settings-button')
    if (tags_options_element.hasClass('disabled')) { tags_options_element.removeClass('disabled') } else tags_options_element.addClass('disabled')
  })

  // Scrub the documents when the "Preview" and "Apply" buttons are pressed
  $('#preview-button').click(function () { scrub('preview') })
  $('#apply-button').click(function () { scrub('apply') })

  // Create the tag options popup when the "Scrub Tags" "Options" button is
  // pressed
  $('#scrub-tags-settings-button').click(function () {
    // Send the request
    $.ajax({type: 'GET', url: 'scrub/get-tag-options'})

    // If the response was successful, create the tag options
      .done(create_tag_options_popup)

    // If the response failed, display an error and "Loading Failed"
    // text
      .fail(function () {
        error('Failed to retrieve the document tags.')
      })
  })

  // Initialize the upload buttons
  initialize_upload_buttons(['lemmas', 'consolidations',
    'stop-words', 'special-characters'])

  // Initialize the tooltips
  initialize_tooltips()

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)
})

/**
 * Creates the tags options popup.
 * @param {string} response The response from the "scrub/get-tags" request.
 * @returns {void}
 */
function create_tag_options_popup (response) {
  // Parse the response
  let tags = parse_json(response)

  // Create the popup
  create_ok_popup('Tag Options')
  let popup_content_element = $('#tag-options-popup .popup-content')

  // If there are no tags, display "No Tags" text and return
  let popup_ok_button_element = $('#tag-options-popup .popup-ok-button')
  if (!tags.length) {
    add_text_overlay('#tag-options-popup .popup-content', 'No Tags')
    popup_ok_button_element.click(close_popup)
    return
  }

  // Otherwise, create the table head and body
  $(`
    <div id="tag-table-head">
      <h3>Tag</h3>
      <h3>Action</h3>
      <h3>Replacement</h3>
    </div>
    <div id=tag-table-body></div>
  `).appendTo(popup_content_element)

  // Create a row for each tag
  for (const tag of tags) {
    // Replace non-alphanumeric characters with dashes
    let formatted_tag = tag[0].replace(/[^A-Za-z0-9 ]/, '-')

    // Create the row element
    let row_element = $(`
      <div class="tag-table-row">
        <h3></h3>
        <div>
          <label><input id="${formatted_tag}-remove-tag-button" type="radio" name="${formatted_tag}_action" value="Remove Tag" checked><span></span>Remove Tag</label>
          <label><input id="${formatted_tag}-remove-element-button" type="radio" name="${formatted_tag}_action" value="Remove Element"><span></span>Remove All</label>
          <label><input id="${formatted_tag}-replace-element-button" type="radio" name="${formatted_tag}_action" value="Replace Element"><span></span>Replace</label>
          <label><input id="${formatted_tag}-leave-alone-button" type="radio" name="${formatted_tag}_action" value="Leave Alone"><span></span>None</label>
        </div>
        <input class="disabled" type="text" spellcheck="false" autocomplete="off" value="${tag[2]}">
      </div>
    `).appendTo('#tag-table-body')

    // Add the HTML-escaped tag name to the row element
    row_element.find('h3').text(tag[0])

    // If the row's "Replace" radio button is selected, enable the
    // "Replacement" input, otherwise disable it
    $(`input[name="${formatted_tag}_action"]`).change(function () {
      let input_element = row_element.find(`input[type="text"]`)
      if ($(this).val() === 'Replace Element') { input_element.removeClass('disabled') } else input_element.addClass('disabled')
    })

    // Get the button name
    let button_name = get_id(tag[1])

    // Check the appropriate option
    row_element.find(`#${formatted_tag}-${button_name}-button`)
      .prop('checked', true).change()
  }

  // Save the tag options when the "OK" button is pressed
  popup_ok_button_element.click(save_tag_options)
}

/**
 * Saves the tag options.
 * @returns {void}
 */
function save_tag_options () {
  // Create the payload
  let rows = $('.tag-table-row')
  let payload = {}

  // For each row in the tag options table...
  for (const row of rows) {
    // Get the tag name and attribute
    let tag = $(row).find('h3').text()
    let attribute = $(row).find(`input[type="text"]`).val()

    // Get the scrubbing action
    let action
    let labels = $(row).find('label input')
    for (const label of labels) { if ($(label).prop('checked')) action = $(label).val() }

    // Add the data to the payload
    payload[tag] = `${action},${tag}`
    payload[`attributeValue${tag}`] = attribute
  }

  // Send a request to save the tag options
  return $.ajax({
    type: 'POST',
    url: 'scrub/save-tag-options',
    data: JSON.stringify(payload),
    contentType: 'application/json; charset=utf-8'
  })

  // If the request is successful, close the popup
    .done(close_popup)

  // If the request failed, display an error
    .fail(function () { error('Failed to save the tag options.') })
}

/**
 * Performs scrubbing on the active documents.
 * @param {string} action The action for the scrub operation (preview or apply).
 * @returns {void}
 */
function scrub (action) {
  // Remove any error messages
  remove_errors()

  // Display the loading overlay and disable the buttons on the document
  // previews section
  start_document_previews_loading()

  // Set the action
  let form_data = new FormData($('form')[0])
  form_data.append('action', action)

  // Send the request
  $.ajax({
    type: 'POST',
    url: 'scrub/execute',
    processData: false,
    contentType: false,
    data: form_data
  })

  // If the request was successful, update the document previews
    .done(update_document_previews)

  // If the request failed, display an error and "Loading Failed"
  // text
    .fail(function () {
      error('Failed to execute the scrubbing. Check the ' +
                'formatting of additional options before retrying.')
      add_text_overlay('#previews', 'Loading Failed')
      enable('#preview-button, #apply-button')
    })
}

/**
 * Updates the document previews.
 * @param {string} response The response containing the new previews.
 * @returns {void}
 */
function update_document_previews (response) {
  let previews = parse_json(response)

  // If there are no previews, display "No Previews" text and return
  if (!previews.length) {
    add_text_overlay('#previews', 'No Previews')
    return
  }

  // Create the previews as hidden elements
  for (const preview of previews) { create_document_preview(preview[0], preview[1]) }

  // Remove the loading overlay, fade in the previews, and enable the
  // buttons for the document previews section
  finish_document_previews_loading()
}

/**
 * Initializes the tooltips.
 * @returns {void}
 */
function initialize_tooltips () {
  // "Scrub Tags"
  create_tooltip('#scrub-tags-tooltip-button', `Handle tags such as
    those used in XML, HTML, or SGML. Click the "Options" button
    to the left to control how each tag will be handled.`)

  // "Keep Hyphens"
  create_tooltip('#keep-hyphens-tooltip-button', `Change all variations of
    Unicode hyphens to a single type of hyphen and leave the hyphens in
    the text. Hyphenated words (e.g., computer-aided) will subsequently
    be treated as one token.`)

  // "Keep Apostrophes"
  create_tooltip('#keep-apostrophes-tooltip-button', `Retain apostrophes
    in contractions and possessives, but not those in plural possessives
    or at the start of a word.`)

  // "Keep Ampersands"
  create_tooltip('#keep-ampersands-tooltip-button', `Leave all ampersands
    in the text. Note that HTML, XML, or SGML entities such as
    "&amp;aelig;" (æ) are handled separately. You can convert these
    entities to standard Unicode characters using the Special Characters
    option below.`)

  // "Lemmas"
  create_tooltip('#lemmas-tooltip-button', `Upload or input a list of
    lemmas (word replacements). Enter the words you want to replace
    separated by comma. Then, add a colon and follow it with the
    replacement word. Enter each set of replacements on a separate line.
    For example, "cyng, kyng:king" will replace every occurrence of "cyng"
    and "kyng" with "king".`)

  // "Consolidations"
  create_tooltip('#consolidations-tooltip-button', `Upload or input a list
    of consolidations (character replacements). Enter the characters you
    want to replace separated by comma. Then, add a colon and follow it
    with the replacement character. Enter each replacement on a separate
    line. For example, "a, b:c" will replace every occurrence of "a" and
    "b" with "c".`)

  // "Stop and Keep Words"
  create_tooltip('#stop-words-tooltip-button', `Upload or input a list of
    "stop words" (words to be removed) or "keep words" (words to keep).
    Separate the words by comma.`)

  // "Special Characters"
  create_tooltip('#special-characters-tooltip-button', `Select a pre-defined
    ruleset or upload or input a list of rules for handling special
    characters such as those in HTML, XML, and SGML. Enter the character
    to replace followed by a comma and then its replacement. Enter each
    replacement on a separate line. For example,"&amp;aelig;, æ" will
    replace "&amp;aelig;" with "æ".`)
}

/**
 * Initializes the upload buttons
 * @param {string[]} names The names of the sections to initialize.
 * @returns {void}
 */
function initialize_upload_buttons (names) {
  // For each of the given sections...
  for (const name of names) {
    // If the "Upload"/"Remove Upload" button is clicked
    let upload_button_element = $(`#${name}-upload-button`)
    upload_button_element.click(function () {
      let file_input_element = $(`#${name}-file-input`)
      let upload_text_element = $(`#${name}-upload-text`)

      // If there is an uploaded file, remove it from the input, remove
      // the displayed file name, and change the "Remove Upload" button
      // to say "Upload" again
      if (file_input_element.val()) {
        file_input_element.val('')
        upload_text_element.addClass('hidden').text('None')
        upload_button_element.text('Upload')
        return
      }

      // Otherwise, create a file selection window
      file_input_element.click()

      // When the file has been selected, display the name of the
      // uploaded file and change the "Upload" button to say
      // "Remove Upload"
      file_input_element.change(function (event) {
        let file = event.target.files[0]
        upload_text_element.text(`Upload: ${file.name}`)
        upload_text_element.removeClass('hidden')
        upload_button_element.text('Remove Upload')
      })
    })
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
      intro: `Welcome to the Scrub page!`,
      position: 'top'
    },
    {
      element: '#scrubbing-options-section',
      intro: `This is the Scrubbing Options section. These are the basic
        scrubbing functions of Lexos. A few recommended options are
        already selected.`,
      position: 'top'
    },
    {
      element: '#preview-button',
      intro: `You can preview your selected scrubbing options here.`,
      position: 'top'
    },
    {
      element: '#apply-button',
      intro: `To make any scrubbing choices permanent to your
        documents, click here.`,
      position: 'top'
    },
    {
      element: '#help-button',
      intro: `For a more in-depth look at this page, visit the Help section.`,
      position: 'bottom'
    },
    {
      element: '#navbar-right',
      intro: `Once you're satisfied with your scrubbed documents, you
        can move on to other pages in Prepare, Visualize, or Analyze.`,
      position: 'bottom'
    },
    {
      intro: `This concludes the Scrub walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
