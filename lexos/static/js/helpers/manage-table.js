var manage_table_documents = []

/**
 * Initializes the manage table.
 * @param {string} parent_query The query for the parent element to create the table in.
 * @param {boolean} enable_context_menu Whether to enable the context menu.
 * @returns {void}
 */
function initialize_manage_table (parent_query, enable_context_menu = false) {
  // Create the table layout
  $(`
        <!-- Manage table head -->
        <div id="manage-table-head">
            <h3 id="active" class="manage-table-cell sortable">Active <i id="state-sortdir" class="sort-by-asc">▲</i></h3>
            <h3 class="manage-table-cell sortable"># <i id="id-sortdir" class="sort-by-asc">▲</i></h3>
            <h3 id="document" class="manage-table-cell sortable">Document <i id="label-sortdir" class="sort-by-asc">▲</i></h3>
            <h3 id="class" class="manage-table-cell sortable">Class <i id="class-sortdir" class="sort-by-asc">▲</i></h3>
            <h3 class="manage-table-cell sortable">Source <i id="source-sortdir" class="sort-by-asc">▲</i></h3>
            <h3 id="excerpt" class="manage-table-cell sortable">Excerpt <i id="preview-sortdir" class="sort-by-asc">▲</i></h3>
            <a id="manage-table-download-button" class="disabled right-justified button" href="manage/download">Download</a>
            <span id="manage-table-tooltip-button" class="tooltip-button">?</span>
        </div>

        <!-- Manage table body -->
        <div id="manage-table-body" class="firefox-hidden-scrollbar"></div>

        <!-- Selection box -->
        <div id="manage-table-selection-box"></div>
    `).appendTo(parent_query)

  // Create the table displaying the uploaded documents
  create_manage_table(enable_context_menu)

  // Initialize the selection box
  initialize_manage_table_selection_box()

  // Toggle selection when the "A" key is pressed
  key_down_callback('A', toggle_manage_table_selection)

  // Initialize the tooltips
  initialize_manage_table_tooltips()
}

/**
 * Creates the table displaying the uploaded documents.
 * @param {boolean} enable_context_menu Whether to enable the context menu.
 * @returns {void}
 */
function create_manage_table (enable_context_menu = true) {
  // Display the loading overlay on the table body
  start_loading('#manage-table-body')

  // Get the uploaded documents
  $.ajax({type: 'GET', url: 'manage/documents'})

  // If the request is successful, create the table
    .done(function (json_response) {
      manage_table_documents = parse_json(json_response)

      // If there are no documents, display "No Documents" text and
      // return
      if (manage_table_documents.length === 0) {
        add_text_overlay('#manage-table-body', 'No Documents')
        return
      }

      // Otherwise, enable the "Download" button
      enable('#manage-table-download-button')

      // Create the table content
      for (let i = 0; i < manage_table_documents.length; ++i) {
        const d = manage_table_documents[i]
        append_manage_table_row(d['id'], i + 1, d['state'],
          d['label'], d['class'], d['source'], d['preview'],
          enable_context_menu)
      }

      // Remove the loading overlay and fade in the table content
      finish_loading('#manage-table-body', '#manage-table-body')
    })

  // Otherwise, display an error
    .fail(function () {
      error('Failed to fetch the documents.')
      add_text_overlay('#manage-table-body', 'Loading Failed')
    })
}

/**
 * Sorts an array of objects. Used for sorting the table.
 * @param {string} key The name of the column to sort by.
 * @param {string} order The sort direction, 'asc' or 'desc'.
 * @returns {void}
 */
function sortArray (key, order = 'asc') {
  return function innerSort (a, b) {
    if (!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) {
      // property doesn't exist on either object
      return 0
    }
    const varA = (typeof a[key] === 'string')
      ? a[key].toUpperCase() : a[key]
    const varB = (typeof b[key] === 'string')
      ? b[key].toUpperCase() : b[key]
    let comparison = 0
    if (varA > varB) {
      comparison = 1
    } else if (varA < varB) {
      comparison = -1
    }
    return (
      (order === 'desc') ? (comparison * -1) : comparison
    )
  }
}

/**
 * Triggers table sorting when a sort arrow is clicked.
 */
$(document).on('click', '.sortable', function () {
  const col = $(this).find('i').attr('id')
  sort_manage_table(manage_table_documents, col)
})

/**
 * Sorts the table displaying the uploaded documents.
 * @param {array} manage_table_documents The list of document row objects.
 * @param {string} col The id of the sort direction arrow.
 * @param {boolean} enable_context_menu Whether to enable the context menu.
 * @returns {void}
 */
function sort_manage_table (manage_table_documents, col, enable_context_menu = true) {
  // Make a copy of the array for sorting
  const copyForSorting = [...manage_table_documents]
  if ($('#' + col).hasClass('sort-by-desc')) {
    copyForSorting.sort(sortArray(col.split('-')[0], 'desc'))
    $('#' + col).removeClass('sort-by-desc').addClass('sort-by-asc').text('▲')
    var reverse = false
  } else {
    copyForSorting.sort(sortArray(col.split('-')[0]))
    $('#' + col).removeClass('sort-by-asc').addClass('sort-by-desc').text('▼')
    reverse = true
  }

  // Create the new table content
  $('#manage-table-body').empty()
  for (let i = 0; i < manage_table_documents.length; ++i) {
    const d = copyForSorting[i]
    let num = i + 1
    if (reverse === true) {
      num = manage_table_documents.length - i
    }
    append_manage_table_row(d['id'], num, d['state'],
      d['label'], d['class'], d['source'], d['preview'],
      enable_context_menu)
  }
}

/**
 * Appends a row to the table.
 * @param {string} id The ID of the document.
 * @param {number} row_number The number of the row.
 * @param {string} active Whether the document is active ("true" or "false").
 * @param {string} label The name of the document.
 * @param {string} class_name The class name of the document.
 * @param {string} source The source name of the document.
 * @param {string} preview The preview of the document.
 * @param {boolean} enable_context_menu Whether to enable the context menu.
 * @returns {void}
 */
function append_manage_table_row (id, row_number, active, label, class_name,
  source, preview, enable_context_menu) {
  // Create a new row and append it to the "table-body" element
  let row = $(`
        <div id="${id}" class="manage-table-row">
            <div class="manage-table-active-indicator"></div>
            <h3 class="manage-table-cell">${row_number}</h3>
            <h3 class="manage-table-cell"></h3>
            <h3 class="manage-table-cell"></h3>
            <h3 class="manage-table-cell"></h3>
            <h3 class="manage-table-cell"></h3>
        </div>
    `).appendTo('#manage-table-body')

  // HTML-escape the text and add it to the row
  $(row.find('.manage-table-cell')[1]).text(label)
  $(row.find('.manage-table-cell')[2]).text(class_name)
  $(row.find('.manage-table-cell')[3]).text(source)
  $(row.find('.manage-table-cell')[4]).text(preview)

  // If the row is active, add the "selected-table-row" class
  if (active) row.addClass('manage-table-selected-row')

  // Add the context menu callback to the row
  if (enable_context_menu) { row.on('contextmenu', show_context_menu) }
}

/**
 * Toggles between selecting and deselecting all documents.
 * @param {event} event The event that triggered the callback.
 * @param {boolean} pressed Whether the key was pressed or released.
 * @returns {void}
 */
function toggle_manage_table_selection (event, pressed) {
  // If a popup is being displayed, return
  if ($('.popup-container:not(#manage-popup)').length) return

  // Check whether all documents are selected
  let all_selected = true
  $('.manage-table-row').each(function () {
    if (!$(this).hasClass('manage-table-selected-row')) { all_selected = false }
  })

  // If all documents are selected, deselect all. Otherwise, select all
  if (all_selected) manage_table_deselect_all()
  else manage_table_select_all()
}

/**
 * Selects all the documents in the table.
 * @returns {void}
 */
function manage_table_select_all () {
  let id_list = []

  // For each row in the table...
  $('.manage-table-row').each(function () {
    // Add the document's ID to "id_list"
    id_list.push($(this).attr('id'))

    // Give the row the class that indicates it is selected
    $(this).addClass('manage-table-selected-row')
  })

  // Send a request to activate all the documents
  send_manage_table_request('activate', id_list)

  // If the request failed, display an error
    .fail(function () { error('Failed to activate the documents.') })
}

/**
 * Deselects all the documents.
 * @returns {void}
 */
function manage_table_deselect_all () {
  let id_list = []

  // For each row in the table...
  $('.manage-table-row').each(function () {
    // Add the document's ID to "id_list"
    id_list.push($(this).attr('id'))

    // Remove the class that indicates the row is selected
    $(this).removeClass('manage-table-selected-row')
  })

  // Send a request to deactivate all the documents
  send_manage_table_request('deactivate', id_list)

  // If the request failed, display an error
    .fail(function () { error('Failed to deactivate the documents.') })
}

/**
 * Gets the document with the given ID.
 * @param {number} id The ID to search for.
 * @returns {Object} The document with the given ID.
 */
function get_manage_document (id) {
  return manage_table_documents.find(function (d) { return d.id === id })
}

/**
 * Initializes the tooltips.
 * @returns {void}
 */
function initialize_manage_table_tooltips () {
  // "Upload List"
  create_tooltip('#manage-table-tooltip-button', `You can manage your
        uploaded files here. Single-click or click and drag to toggle whether
        documents are active. Right-click for more options.`, true)
}

/**
 * Disables the "Download" button, sends a request, updates the document count
 *      and re-enables the "Download" button.
 * @param {string} url: The URL to send the request to.
 * @param {object} payload: The JSON payload to send.
 * @param {boolean} update_active_count: Whether to update the number of
 *      active documents.
 * @returns {jqXHR}: The jQuery request object.
 */
function send_manage_table_request (url, payload = '', update_active_count = true) {
  // Disable the download button
  disable('#manage-table-download-button')

  // Send the request
  return $.ajax({
    type: 'POST',
    url: 'manage/' + url,
    data: JSON.stringify(payload),
    contentType: 'application/json; charset=utf-8'
  })

    // If the request is successful...
    .done(function () {
      // Update the number of active documents if desired
      if (!update_active_count) return
      update_active_document_count()
        .done(function (response) {
          // If there is at least one active document, enable the
          // "Download" button
          if (parseInt(response) >= 1) { enable('#manage-table-download-button') }
        })
    })
}
