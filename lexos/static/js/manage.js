let context_menu_document_id

$(function () {
  // Create the manage table
  initialize_manage_table('#manage-table', true)

  // Create the context menu hide callbacks
  $(window).on('mousedown resize', hide_context_menu)
  $('#main-section').on('scroll', hide_context_menu)

  // Create the context menu button callbacks
  $('#preview-button').mousedown(preview)
  $('#edit-name-button').mousedown(edit_name)
  $('#edit-class-button').mousedown(edit_class)
  $('#delete-button').mousedown(delete_document)
  $('#merge-selected-button').mousedown(merge_selected)
  $('#edit-selected-classes-button').mousedown(edit_selected_classes)
  $('#delete-selected-button').mousedown(delete_selected)
  $('#select-all-button').mousedown(manage_table_select_all)
  $('#deselect-all-button').mousedown(manage_table_deselect_all)

  // Initialize the walkthrough
  initialize_walkthrough(walkthrough)

  // Disable the "Active Documents" button
  $('#active-documents-text').css('pointer-events', 'none')
})

/**
 * Shows a custom context menu.
 * @param {Event} event The event that triggered the callback.
 * @returns {void}
 */
function show_context_menu (event) {
  // Prevent the default context menu from appearing
  event.preventDefault()

  // Save the ID of the right-clicked document for use in other functions
  context_menu_document_id = parseInt($(this).attr('id'))

  // Set the custom context menu's position to the right-click and make it
  // visible and clickable
  let position = get_mouse_position(event)

  let page_size = get_page_size()
  let context_menu_size = get_element_size('#context-menu')
  let context_menu_far_position = point_add(position, context_menu_size)

  if (context_menu_far_position.x > page_size.x) { position.x -= context_menu_size.x }

  if (context_menu_far_position.y > page_size.y) { position.y -= context_menu_size.y }

  $('#context-menu').css({'pointer-events': 'auto',
    'opacity': '1',
    'left': `${position.x}px`,
    'top': `${position.y}px`})
}

/**
 * Hides the custom context menu.
 * @param {Event} event The event that triggered the callback.
 * @returns {void}
 */
function hide_context_menu (event) {
  $('#context-menu').css({'pointer-events': 'none', 'opacity': '0'})
}

/**
 * Creates a popup containing a preview of the document that was right-clicked.
 * @returns {void}
 */
function preview () {
  // Send a request to get the preview of the document that was right-clicked
  send_manage_table_request('preview', context_menu_document_id)

  // If the request is successful create a popup and append the
  // HTML-escaped document preview to it
    .done(function (response) {
      create_popup('Preview')
      let preview = $(`<h3 id="document-preview-text"></h3>`)
        .appendTo('#preview-popup .popup-content')
      preview.text(parse_json(response)['preview_text'])
    })

  // If the request failed, display an error
    .fail(function () {
      error(`Failed to retrieve the document's preview.`)
    })
}

/**
 * Renames the document that was right-clicked.
 * @returns {void}
 */
function edit_name () {
  // Create a popup containing a text input
  create_text_input_popup('Document Name')

  // Set the popup's initial text input to the existing document name
  $('#document-name-popup .popup-input').val(
    get_manage_document(context_menu_document_id).label)

  // If the popup's "OK" button is clicked
  $('#document-name-popup .popup-ok-button').click(function () {
    // Make a request to set the name of the document that was
    // right-clicked to the content of the popup's text input field
    send_manage_table_request('edit-name', [context_menu_document_id,
      $('#document-name-popup .popup-input').val()])

    // If the request was successful, close the popup and recreate the
    // table
      .done(function () { close_popup(); create_manage_table() })

    // If the request failed, display an error
      .fail(function () { error("Failed to edit the document's name.") })
  })
}

/**
 * Sets the class name of the document that was right-clicked.
 * @returns {void}
 */
function edit_class () {
  // Create a popup containing a text input
  create_text_input_popup('Document Class')

  // Set the popup's initial text input to the existing document class
  $('#document-class-popup .popup-input').val(
    get_manage_document(context_menu_document_id).class)

  // When the popup's "OK" button is clicked
  $('#document-class-popup .popup-ok-button').click(function () {
    // Make a request to set the class of the document that was
    // right-clicked to the content of the popup's text input field
    send_manage_table_request('set-class', [context_menu_document_id,
      $('#document-class-popup .popup-input').val()])

    // If the request was successful, close the popup and recreate the
    // table
      .done(function () { close_popup(); create_manage_table() })

    // If the request failed, display an error
      .fail(function () { error("Failed to set the document's class.") })
  })
}

/**
 * Deletes the document that was right-clicked.
 * @returns {void}
 */
function delete_document () {
  // Send a request to delete the document that was right-clicked
  send_manage_table_request('delete', context_menu_document_id)

  // If the request was successful, recreate the table
    .done(function () { create_manage_table() })

  // If the request failed, display an error
    .fail(function () { error('Failed to delete the document.') })
}

/**
 * Merges the selected documents.
 * @returns {void}
 */
function merge_selected () {
  let selected_document_ids = get_selected_document_ids()
  let first_selected_document =
        get_manage_document(selected_document_ids[0])

  // Create the popup
  create_ok_popup('Merge Active')
  $(`
    <h3>Name: </h3>
    <input id="merge-name-input" value="Merge-${first_selected_document.label}" type="text" spellcheck="false" autocomplete="off">
    <br>
    <label>
        <input id="merge-milestone-checkbox" name="" type="checkbox">
        <span></span>
        Milestone:
        <input id="merge-milestone-input" name="" value="#EOF#" type="text" spellcheck="false" autocomplete="off">
    </label>
  `).appendTo('#merge-active-popup .popup-content')

  // If the popup's "OK" button is clicked...
  $('#merge-active-popup .popup-ok-button').click(function () {
    // Create the payload
    let payload = [
      selected_document_ids,
      $('#merge-name-input').val(),
      first_selected_document.source,
      $('#merge-milestone-checkbox').is(':checked')
        ? $('#merge-milestone-input').val() : ''
    ]

    // Send the merge request
    send_manage_table_request('merge-selected', payload)

      // If the request was successful, close the popup and recreate the
      // table
      .done(function () { close_popup(); create_manage_table() })

      // If the request failed, display an error
      .fail(function () {
        error('Failed to merge the active documents.')
      })
  })
}

/**
 * Edits the class names of the selected documents.
 * @returns {void}
 */
function edit_selected_classes () {
  // Create a popup containing a text input
  create_text_input_popup('Document Class')

  // If the popup's "OK" button is clicked...
  $('#document-class-popup .popup-ok-button').click(function () {
    // Send a request to set the class names of the selected documents
    // to the value in the popup's text input
    send_manage_table_request('edit-selected-classes',
      [get_selected_document_ids(),
        $('#document-class-popup .popup-input').val()])

      // If the request was successful, close the popup and recreate the
      // table
      .done(function () { close_popup(); create_manage_table() })

      // If the request failed, display an error
      .fail(function () {
        error("Failed to edit the active documents' classes.")
      })
  })
}

/**
 * Deletes the selected documents.
 * @returns {void}
 */
function delete_selected () {
  // Send a request to delete the selected documents
  send_manage_table_request('delete-selected')

    // If the request was successful, recreate the table
    .done(function () { create_manage_table() })

    // If the request failed, display an error
    .fail('Failed to delete the active documents')
}

/**
 * Gets the IDs of the currently selected documents.
 * @returns {Number[]}: The selected document IDs.
 */
function get_selected_document_ids () {
  let id_list = []
  $('.manage-table-row').each(function () {
    if ($(this).hasClass('manage-table-selected-row')) { id_list.push(parseInt($(this).attr('id'))) }
  })

  return id_list
}

/**
 * Initializes the walkthrough.
 * @returns {void}
 */
function walkthrough () {
  let intro = introJs()
  intro.setOptions({steps: [
    {
      intro: `Welcome to the Manage page!`,
      position: 'top'
    },
    {
      element: '#active',
      intro: `Active documents will have a blue highlight to them. You
        can activate and deactivate documents by clicking.`,
      position: 'bottom'
    },
    {
      element: '#document',
      intro: `The Document column holds custom document names. You can
        rename documents by right-clicking.`,
      position: 'bottom'
    },
    {
      element: '#class',
      intro: `If you want to group documents together, you may give them
        a class by right-clicking.`,
      position: 'bottom'
    },
    {
      element: '#excerpt',
      intro: `Excerpt will give you a preview of your document.`,
      position: 'bottom'
    },
    {
      element: '#active-documents-footer',
      intro: `On any other page, you can activate and deactivate
        documents by clicking "Active Documents" in the lower right
        corner.`,
      position: 'top'
    },
    {
      element: '#help-button',
      intro: `For a more in-depth look at this page, visit the Help section.`,
      position: 'bottom'
    },
    {
      element: '#prepare-button',
      intro: `Once you're satisfied with your active documents, you can
        move on to the "Prepare" pages.`,
      position: 'bottom'
    },
    {
      intro: `This concludes the Manage walkthrough!`,
      position: 'top'
    }
  ]})

  return intro
}
