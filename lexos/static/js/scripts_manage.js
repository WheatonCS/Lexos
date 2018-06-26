/**
 * Initialize the data Table
 * @return {void}
 */
$(function () {
  const table = initTable() // function to initialize the table.
  tableAction(table)
})

/**
 * @return {object} table - initialize the table
 * Change the element name and test whether the table variable persists
 * */
function initTable () {
  return $('#demo').DataTable({
    paging: true,
    scrollY: 400,
    autoWidth: false,
    searching: true,
    destroy: true,
    ordering: true,
    select: true,
    'initComplete': function () {
      // enables area selection extension
      $('#demo').AreaSelect()
    },
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, 'All']],
    pageLength: 5,
    scrollCollapse: true,
    dom: '<\'row\'<\'col-sm-6\'l><\'col-sm-6 pull-right\'f>>' +
    '<\'row\'<\'col-sm-12\'rt>>' +
    '<\'row\'<\'col-sm-5\'i><\'col-sm-7\'p>>',
    buttons:
      ['copy', 'excel', 'pdf'],
    language: {
      lengthMenu: 'Display _MENU_ documents',
      info: 'Showing _START_ to _END_ of _TOTAL_ documents',
      zeroRecords: 'No documents to display',
      select: {
        rows: ''
      }
    },
    columnDefs: [
      {width: '15', sortable: false, class: 'index', targets: 0},
      {width: '150', type: 'natural', targets: [1, 2, 3]}
    ],
    order: [[1, 'asc']]
  })
}

/**
 * This function calls upon different functions when the user clicks the three
 * button on top-right of the table. buttons: "Select All", "Deselect All" and "Delete Selected"
 * @param {object} table - table object
 * @return {void}
 */
function tableAction (table) {
  registerColumn(table) // Draw the table column and make it searchable.

  /* Add all rows with .selected to the DataTables activeRows array
   It does not appear that this array needs to be maintained after
   initialisation, but the code to do so is commented out for de-bugging. */
  let activeRows = []
  $(table).find('tbody tr').each(function (index) {
    if ($(this).hasClass('selected')) {
      let i = ':eq(' + index + ')'
      table.rows(i).select()
      activeRows.push($(this).attr('id'))
    }
    // Show the download button if there is at least 1 active file.
    if (activeRows.length !== 0) {
      $('#bttn-downloadSelectedDocs').show()
    }
  })

  $('.col-sm-5').append('<p style=\'display:inline; float:left; width:200px !important;\' id=\'name\'></p>')
  // LEGACY CODE: Data tables active documents counter wasn't working.
  // I wrote a new way to do this. First, append an inline p tag to where the default counter used to be before I took it out
  // NOTE the p is cleared when going to a new page of the table. To fix this, datatables.js must be made local and changed.

  registerSelectEvents(table)
  // Perform the different right click options on the document.
  tableDocumentActions(table)

  // Call Save function on click.
  $('#save').click(function () {
    saveFunction(table)
  })
  // Call Delete function on click.
  $('#delete').click(function () {
    let selectedRows = table.rows({selected: true}).nodes().to$()
    deleteAllSelected(selectedRows, table)
  })

  // Trigger selection buttons
  $('#selectAllDocs').click(function () { selectAll(table) })
  $('#deselectAllDocs').click(function () { deselectAll(table) })
  $('#deleteSelectedDocs').click(function () {
    let selectedRows = table.rows({selected: true}).nodes().to$()
    deleteAllSelected(selectedRows, table)
  })
  // Remove the footer from alert modals when hidden
  $('#alert-modal').on('hidden.bs.modal', function () {
    $('#alert-modal').find('.modal-footer').remove()
  })
}

/**
 * Enable search and ordering in the table within the document.
 * @param {object} table - table object
 * @return{void}
 */
function registerColumn (table) {
  // Draw the index column
  table.on('order.dt search.dt', function () {
    table
    // 0 corresponds to the index column
      .column(0, {
        search: 'applied',
        order: 'applied'
      }
      )
      .nodes()
      .each(function (cell, i) {
        cell.innerHTML = i + 1
      })
  })
    .draw()

  // Make all columns searchable
  table.on('order.dt search.dt', function () {
    table
    // 1 corresponds to the 'Document Name' column
      .column(1, {
        search: 'applied',
        order: 'applied'
      }
      )
      // 2 corresponds to the 'Original Source' column
      .column(2, {
        search: 'applied',
        order: 'applied'
      }
      )
      // 3 corresponds to the 'Excerpt' column
      .column(3, {
        search: 'applied',
        order: 'applied'
      }
      )
  })
    .nodes()
    .draw()
}

/**
 * selection and deselection of the table rows.
 * @param {object} table - table object
 * @return {void}
 * */
function registerSelectEvents (table) {
  table
    .on('select', function (e, dt, type, indexes) {
      // Get selected rows as a jQuery object
      const selectedRows = table.rows(indexes).nodes().to$()
      // Call the ajax function
      enableRows(selectedRows, table)
      handleSelectButtons(table)
      $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have ' + table.rows('.selected').data().length + ' active document(s)'
      document.getElementById('name').innerHTML = table.rows('.selected').data().length + ' active documents' // add the correct counter text to the p
      $('#bttn-downloadSelectedDocs').show()
    })
    .on('deselect', function (e, dt, type, indexes) {
      // Get deselected rows as a jQuery object
      const deselectedRows = table.rows(indexes).nodes().to$()
      // Call the ajax function
      disableRows(deselectedRows, table)
      handleSelectButtons(table)
      document.getElementById('name').innerHTML = table.rows('.selected').data().length + ' active documents' // same as the other one
      $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have ' + table.rows('.selected').data().length + ' active document(s)'
      if (table.rows('.selected').data().length === 0) {
        $('#bttn-downloadSelectedDocs').hide()
      }
    })
}

/***
 * Right click options on the documents
 * @param {object} table - table object
 * @return {void}
 */
function tableDocumentActions (table) {
  handleSelectButtons(table)
  let selectedRows
  $('#demo').contextmenu({
    target: '#context-menu',
    scopes: 'td',
    before: function () {
      prepareContextMenu(table)
    },
    onItem: function (cell, e) {
      let target = cell.parent().attr('id')
      let action = $(e.target).attr('data-context')
      switch (action) {
        case 'preview':
          showPreviewText(target)
          break
        case 'edit_doc_name':
          editName(target)
          break
        case 'edit_doc_class':
          editClass(target)
          break
        case 'clone_doc':
          // clone(target);
          break
        case 'delete_doc':
          deleteDoc(target, table)
          break
        case 'select_all':
          selectAll(table)
          break
        case 'deselect_all':
          deselectAll(table)
          break
        case 'merge_selected':
          selectedRows = table.rows({selected: true}).nodes().to$()
          mergeSelected(cell, selectedRows)
          break
        case 'apply_class_selected':
          selectedRows = table.rows({selected: true}).nodes().to$()
          applyClassSelected(cell, selectedRows)
          break
        case 'delete_all_selected':
          selectedRows = table.rows({selected: true}).nodes().to$()
          deleteAllSelected(selectedRows, table)
          break
      }
    }
  })
  // Refresh context menu on show
  $('#context-menu').on('show.bs.context', function () {
    prepareContextMenu(table)
  })
}

/***
 * "Save" button for the right click options on the document.
 * Save button in pop-up modal.
 * @param {object} table - table object
 * @return {void}
 */
function saveFunction (table) {
  const merge = $('#merge').val()
  let rowId = $('#tmp-row').val()
  const column = $('#tmp-column').val()
  const value = $('#tmp').val()
  let rowIds
  let source
  let milestone
  if (rowId.match(/,/)) {
    rowIds = rowId.split(',')
    source = $('#' + rowId).children().eq(3).text()
    if (merge === 'true') {
      if ($('#addMilestone').prop('checked') === true) {
        milestone = $('#milestone').val()
      } else {
        milestone = ''
      }
      mergeDocuments(rowIds, column, source, value, milestone, table)
    } else {
      saveMultiple(rowIds, column, value, table)
    }
  } else {
    saveOne(rowId, column, value, table)
  }
}

// Handle the milestone checkbox in the document merge modal
$(document).on('change', $('#addMilestone'), function () {
  $('#milestoneField').toggle()
})


/* S U P P O R T I N G    F U N C T I O N S */

/***
 * Shows or hides the Active Documents icon in response to the table state
 * Folder icon on the top right of the navigation bar.
 * @param {object} table - table object
 * @return {void}
 */
function toggleActiveDocsIcon (table) {
  // Hide the active docs icon if there are no docs selected
  const openFolder = $('.fa-folder-open-o')
  if (table.rows({selected: true}).ids().length < 1) {
    openFolder.fadeOut(200)
  } else {
    openFolder[0].dataset.originalTitle = 'You have ' + table.rows({selected: true}).ids().length + ' active document(s)'
    openFolder.fadeIn(200)
  }
}

/***
 * Sets the status of all the documents in File manager as 'selected'
 * @param {object} table - table object
 * @return {void}
 */
function selectAll (table) {
  const url = '/selectAll'
  sendAjaxRequestSelectAll(url)
    .done(
      function () {
        // Select All Rows in the UI
        table.rows().select()
        handleSelectButtons(table)
        toggleActiveDocsIcon(table)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html('Lexos could not select all the documents.')
        errorModal.modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

/***
 * @param {string} url - url to the page.
 * @return {object} ajax - XMLHttpRequest object
 */
function sendAjaxRequestSelectAll (url) {
  return $.ajax({
    type: 'POST',
    url: url
  })
}

/***
 * deselects all the document in file manager.
 * @param {object} table - table object
 * @return {void}
 */
function deselectAll (table) {
  const url = '/deselectAll'
  sendAjaxRequestDeselect(url)
    .done(
      function () {
        // Deselect All Rows in the UI
        table.rows().deselect(table)
        handleSelectButtons(table)
        toggleActiveDocsIcon(table)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html('Lexos could not deselect all the documents.')
        errorModal.modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

/***
 * @param {string} url - url to the page
 * @return {object} ajax - XMLHttpRequest object
 */
function sendAjaxRequestDeselect (url) {
  return $.ajax({
    type: 'POST',
    url: url
  })
}

/* #### enableRows() #### */

// Enables selected rows in the File Manager and sets UI to selected.
/***
 * Enables selected rows in the File Manager by setting the status of the
 * rows as  selected.
 * @param {array} selectedRows - rows matched by the selector
 * @param {object} table - table object
 * @return {void}
 */
function enableRows (selectedRows, table) {
  let fileIds = []
  selectedRows.each(function () {
    fileIds.push($(this).attr('id'))
  })
  // Ensure fileIds contains unique entries
  fileIds = unique(fileIds)
  // Convert the fileIds list to a json string for sending
  const data = JSON.stringify(fileIds)
  const url = '/enableRows'
  sendAjaxRequestEnableRows(url, data)
    .done(function () {
      handleSelectButtons(table)
      toggleActiveDocsIcon(table)
    })
    .fail(function (textStatus, errorThrown) {
      const errorModal = $('#error-modal')
      errorModal.find('.modal-body').html('Lexos could not select the requested documents.')
      errorModal.modal()
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    })
}

/***
 *
 * @param {string} url - url for the page.
 * @param {string} data - file ids
 * @return {object} ajax - XMLHttpRequest object
 */
function sendAjaxRequestEnableRows (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/***
 * Deselects the row.
 * @param {array} deselectedRows - rows matched by the selector.
 * @param {object} table - table object
 * @return {void}
 */
function disableRows (deselectedRows, table) {
  let fileIds = []
  deselectedRows.each(function () {
    fileIds.push($(this).attr('id'))
  })
  // Ensure fileIds contains unique entries
  fileIds = unique(fileIds)
  // Convert the fileIds list to a json string for sending
  const url = '/disableRows'
  let data = JSON.stringify(fileIds)
  sendAjaxRequestDisableRow(url, data)
    .done(
      function () {
        handleSelectButtons(table)
        toggleActiveDocsIcon(table)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html('Lexos could not deselect the requested documents.')
        errorModal.modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

/***
 * @param {string}  url  - url for the page
 * @param {string}  data - file ids
 * @return {object} ajax - XMLHttpRequest Object
 */
function sendAjaxRequestDisableRow (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/***
 * right click option for context menu
 * @param {string} rowId -  value attribute of the selected elements.
 * @return {void}
 */
function showPreviewText (rowId) {
  const url = '/getPreview'
  sendAjaxRequestPreview(url, rowId)
    .done(
      function (response) {
        response = JSON.parse(response)
        const title = 'Preview of <b>' + response['label'] + '</b>'
        let text = response['previewText']
        // Encode tags as HTML entities
        text = String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
        //* To Do: Convert tagged texts to strings
        $('.modal-title').html(title)
        $('#preview_text').html(text)
        $('#preview').modal()
      })
    .fail(function (jqXHR, textStatus, errorThrown) {
      const errorModal = $('#error-modal')
      errorModal.find('.modal-body').html('Lexos could not retrieve the file preview.')
      errorModal.modal()
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    })
}

/***
 * @param {string} url - url for the page
 * @param {string} rowId -  value attribute of the selected elements.
 * @return {object} ajax - XMLHttpRequest object
 */
function sendAjaxRequestPreview (url, rowId) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: rowId,
    contentType: 'charset=UTF-8'
  })
}

/***
 * Edit the name of the document.
 * @param {string} rowId -  value attribute of the selected elements.
 * @return {void}
 */
function editName (rowId) {
  $('#edit-form').remove()
  let cellName = $('#' + rowId).find('td:eq(1)').text()
  let form = '<div id="edit-form">Document Name <input id="tmp" type="text" value="' + cellName + '">'
  form += '<input id="tmp-row" type="hidden" value="' + rowId + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="1"></div>'
  $('#edit_title').html('Edit Name of <b>' + cellName + '</b>')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/***
 * Edit the Class name.
 * @param {string} rowId -  value attribute of the selected elements.
 * @return {void}
 */
function editClass (rowId) {
  $('#edit-form').remove()
  let docName = $('#' + rowId).find('td:eq(1)').text()
  let cellValue = $('#' + rowId).find('td:eq(2)').text()
  let form = '<div id="edit-form">Class Label <input id="tmp" type="text" value="' + cellValue + '">'
  form += '<input id="tmp-row" type="hidden" value="' + rowId + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="2"></div>'
  $('#edit_title').html('Edit <b>' + docName + '</b> Class')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/* #### mergeSelected() #### */
/***
 * Merges the selected documents.
 * @param {array} cell - contains the columns and rows index
 * @param {array} selectedRows - rows matched by the selector
 * @return {void}
 */
function mergeSelected (cell, selectedRows) {
  let rowIds = []
  selectedRows.each(function () {
    let id = $(this).attr('id')
    rowIds.push(id)
  })
  $('#edit-form').remove()
  let cellValue = 'merge-' + $('#' + rowIds[0]).find('td:eq(1)').text()
  let form = '<div id="edit-form">New Document Name '
  form += '<input id="tmp" type="text" value="' + cellValue + '"><br>'
  form += '<input id="addMilestone" type="checkbox"> Add milestone at end of documents'
  form += '<span id="milestoneField" style="display:none;">'
  form += '<br>Milestone <input id="milestone" type="text" value="#EOF#"></span>'
  form += '<input id="merge" type="hidden" value="true">'
  form += '<input id="tmp-row" type="hidden" value="' + rowIds + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="2"></div>'
  $('#edit_title').html('Merge Selected Documents')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/***
 *
 * @param {array} cell - contains the columns and rows index
 * @param {array} selectedRows - rows matched by the selector
 * @return {void}
 */
function applyClassSelected (cell, selectedRows) {
  let rowIds = []
  selectedRows.each(function () {
    let id = $(this).attr('id')
    rowIds.push(id)
  })
  $('#edit-form').remove()
  const cellValue = cell.text()
  let form = '<div id="edit-form">Class Label <input id="tmp" type="text" value="' + cellValue + '">'
  form += '<input id="tmp-row" type="hidden" value="' + rowIds + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="2"></div>'
  $('#edit_title').html('Apply <b>' + cellValue + '</b> Class to Selected Documents')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/* #### mergeDocuments() #### */

// Helper function saves value in edit dialog and updates table with a new document
/***
 * Merges the document and updates the table with a new document.
 * @param {array} rowIds - value attribute of the selected elements.
 * @param {string} column - not sure what this is exactly for.
 * @param {string} source - name of the document.
 * @param {string} value - name of the merged document.
 * @param {string} milestone - name of the milestone.
 * @param {object} table - table object
 * @return{void}
 */
function mergeDocuments (rowIds, column, source, value, milestone, table) {
  const url = '/mergeDocuments'
  let data = JSON.stringify([rowIds, value, source, milestone])

  // Do Ajax
  sendAjaxRequestMergedocuments(url, data)
    .done(
      function (response) {
        const table = $('#demo').DataTable()
        response = JSON.parse(response)
        let newIndex = response[0]
        // let newIndex = parseInt(rowIds.slice(-1)[0])+1;
        table.rows().deselect(table)
        let text = response[1].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
        let rowNode = table.row
          .add([newIndex, value, '', source, text])
          .draw(false)
          .node()
        table.rows(newIndex).select(table) // This automatically calls enableRows()
        $(rowNode)
          .attr('id', newIndex)
          .addClass('selected')
        $(rowNode).children().first().css('text-align', 'right')
        handleSelectButtons(table)
        $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have 1 active document(s)'
        // toggleActiveDocsIcon();
        $('#edit-modal').modal('hide')
        $('#edit-form').remove()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html('Lexos could not merge the requested documents or could not save the merged document.')
        errorModal.modal()
        $('#edit-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

/***
 *
 * @param {string} url - url for the page.
 * @param {string}  data - file ids
 * @return {object} ajax - XMLHttpRequest object
 */
function sendAjaxRequestMergedocuments (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/***
 * Helper function saves value in edit dialog and updates table for multiple rows
 * @param {array} rowIds - value attribute of the selected elements.
 * @param {string} column - not sure
 * @param {string} value - name that the user inputs.
 * @param {object} table - table object
 * @return {void}
 */
function saveMultiple (rowIds, column, value, table) {
  // Prepare data and request
  const url = '/setClassSelected'
  let data = JSON.stringify([rowIds, value])
  // Do Ajax
  sendAjaxRequestSaveMultiple(url, data)
    .done(
      function (response) {
        rowIds = JSON.parse(response)
        // Update the UI
        let reloadPage = false
        $.each(rowIds, function (i) {
          let id = '#' + rowIds[i]
          $(id).find('td:eq(2)').text(value)
          if ($(id).length === 0) {
            reloadPage = true
          }
        })
        $('#edit-modal').modal('hide')
        $('#edit-form').remove()
        // Ugly hack to make sure rows are updated across table pages
        if (reloadPage === true) {
          window.location.reload()
        } else {
          toggleActiveDocsIcon(table)
          table.draw()
        }
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html('Lexos could not update the class of the requested documents.')
        errorModal.modal()
        $('#delete-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

/***
 * @param {string} url - url for the page.
 * @param {string} data - row id and name the user types in.
 * @return {object} ajax - XMLHttpRequest Object.
 */
function sendAjaxRequestSaveMultiple (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/***
 * Helper function saves value in edit dialog and updates table
 * @param {string} rowId - value attribute of the selected elements.
 * @param {object} column - value attribute of the selected elements.
 * @param {object} value - value attribute of the selected elements.
 * @param {object} table - table object
 * @return {boolean} - return false if the name of the document is empty
 */
function saveOne (rowId, column, value, table) {
  // Validation - make sure the document name is not left blank
  if (column === 1 && value === '') {
    let msg = '<p>A document without a name is like coffee without caffeine!</p><br>'
    msg += '<p>Make sure you don\'t leave the field blank.</p>'
    const alertModal = $('#alert-modal')
    alertModal.find('.modal-body').html(msg)
    alertModal.modal()
    let revert = $('#' + rowId).find('td:eq(1)').text()
    $('#tmp').val(revert)
    return false
  }
  // Prepare data and request
  let data = JSON.stringify([rowId, value])
  let url = ''
  let errorMsg
  switch (column) {
    case '1':
      url = '/setLabel'
      errorMsg = 'Lexos could not update the document name.'
      break
    case '2':
      url = '/setClass'
      errorMsg = 'Lexos could not update the document class.'
      break
  }
  sendAjaxRequestSaveOne(url, data)
    .done(
      function () {
        // Update the UI
        let cell = 'td:eq(' + column + ')'
        $('#' + rowId).find(cell).text(value)
        $('#edit-modal').modal('hide')
        $('#edit-form').remove()
        table.draw()
        toggleActiveDocsIcon(table)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html(errorMsg)
        errorModal.modal()
        $('#edit-form').remove()
        $('#edit-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

/***
 * @param {string} url - empty string
 * @param {string} data - json string data
 * @return {object} ajax- XMLHttpRequest object
 */
function sendAjaxRequestSaveOne (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/***
 * Helper function deletes selected row and updates table
 * @param {string} rowId -  value attribute of the selected elements.
 * @param {object} table - table object
 * @return {void}
 */
function deleteOne (rowId, table) {
  const url = '/deleteOne'
  sendAjaxRequestDeleteOne(url, rowId)
    .done(
      function () {
        // Update the UI
        let id = '#' + rowId
        table.row(id).remove()
        handleSelectButtons(table)
        toggleActiveDocsIcon(table)
        table.draw()
      })
    .fail(function (jqXHR, textStatus, errorThrown) {
      const errorModal = $('#error-modal')
      errorModal.find('.modal-body').html('Lexos could not delete the requested document.')
      errorModal.modal()
      $('#delete-modal').modal('hide')
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    })
}

/**
 * @param {string} url - url of thepage
 * @param {string} rowId -  value attribute of the selected elements.
 * @return {object} ajax - XMLHttpRequest object
 */
function sendAjaxRequestDeleteOne (url, rowId) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: rowId,
    contentType: 'charset=UTF-8',
    cache: false
  })
}

/***
 * Delete the selected document.
 * @param {string} rowId -  value attribute of the selected elements.
 * @param {object} table - table object
 * @return {void}
 */
function deleteDoc (rowId, table) {
  let docName = $('#' + rowId).find('td:eq(1)').text()
  let html = '<p>Are you sure you wish to delete <b>' + docName + '</b>?</p>'
  html += '<span id="deleteId" style="display:none;">' + rowId + '</span>'
  let footer = '<div class="modal-footer"><button type="button" data-dismiss="modal" class="btn btn-primary" id="confirm-delete-bttn" style="margin-left:2px;margin-right:2px;">Delete</button><button type="button" data-dismiss="modal" class="btn" style="margin-left:2px;margin-right:2px;">Cancel</button></div>'
  const deleteModal = $('#delete-modal')
  deleteModal.find(".modal-body").html(html)
  deleteModal.find(".modal-body").append(footer)
  deleteModal.modal()
    .one('click', '#confirm-delete-bttn', function () {
      rowId = $('#deleteId').text()
      deleteOne(rowId, table)
    })
}

/**
 * Helper function deletes selected rows and updates table
 * @param {object} rowIds -  value attribute of the selected elements.
 * @param {object} table - table object
 * @return {void}
 */
function deleteSelected (rowIds, table) {
  const url = '/deleteSelected'
  sendajaxRequestDeleteSelected(url, rowIds)
    .done(
      function (response) {
        // Update the UI
        rowIds = JSON.parse(response)
        // rowIds = rowIds.split(",");
        $.each(rowIds, function (i) {
          let id = '#' + rowIds[i]
          table.row(id).remove()
        })
        handleSelectButtons(table)
        toggleActiveDocsIcon(table)
        table.draw()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        const errorModal = $('#error-modal')
        errorModal.find('.modal-body').html('Lexos could not delete the requested documents.')
        errorModal.modal()
        $('#delete-modal').modal('hide')
        console.log('bad: ' + textStatus + ' : ' + errorThrown)
      })
}

/**
 * Ajax call to delete the selected documents.
 * @return {object} ajax- XMLHttpRequest object
 * @param {string} url - url of the page
 * @param {object} rowIds -  value attribute of the selected elements.
 */
function sendajaxRequestDeleteSelected (url, rowIds) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: rowIds,
    contentType: 'charset=UTF-8',
    cache: false
  })
}

/**
 * deletes all the selected rows.
 * @param {array} selectedRows - array of rows that have been selected
 * @param {object} table - table object
 * @return {void}
 */
function deleteAllSelected (selectedRows, table) {
  const deleteDiv = $('#delete-modal')
  const deleteModal = deleteDiv.find('.modal-body')
  let rowIds = []
  selectedRows.each(function () {
    let id = $(this).attr('id')
    rowIds.push(id)
  })
  let html = '<p>Are you sure you wish to delete the selected documents?</p>'
  html += '<span id="deleteIds" style="display:none;">' + rowIds.toString() + '</span>'
  let footer = '<div class="modal-footer"><button type="button" data-dismiss="modal" class="btn btn-primary" id="confirm-delete-bttn" style="margin-left:2px;margin-right:2px;">Delete</button><button type="button" data-dismiss="modal" class="btn" style="margin-left:2px;margin-right:2px;">Cancel</button></div>'
  deleteModal.html(html)
  deleteModal.append(footer)
  deleteDiv.modal()
    .one('click', '#confirm-delete-bttn', function () {
      const rowIds = $('#deleteIds').text()
      deleteSelected(rowIds, table)
    })
}

/**
 * Helper function ensures id lists have no duplicates
 * @return {array} fileIds - indexes
 * @param {array} fileIds - array of file ids
 */
function unique (fileIds) {
  return $.grep(fileIds, function (el, index) {
    return index === $.inArray(el, fileIds)
  })
}

/**
 * Helper function to change configure the context menu based on
 * the number of rows currently selected
 * @param {object} table - table object
 * @return {void}
 */
function prepareContextMenu (table) {
  const contextMenu = $('#context-menu')
  // Refresh all options
  contextMenu.find('li').removeClass('disabled')
  contextMenu.find('li').find('a').removeProp('disabled')

  // Comparison values
  let numRows = table.rows().ids().length
  let numRowsSelected = table.rows('.selected').data().length
  // Set config options -- Numbers refer to li elements, including dividers
  // The numbers below corresponds to the different options in right lick
  // on the document.
  let opts
  switch (true) {
    /*
    5: 'Select All Documents'
    6: 'Deselect All Documents
    8: 'Merge Selected Documents'
    9: 'Apply Class to Selected Documents'
    10: 'Delete Selected Documents' */

    case numRowsSelected === 0: // No rows selected
      opts = [6, 8, 9, 10]
      break
    case numRowsSelected === 1: // 1 row selected
      opts = [8, 9]
      break
    case numRowsSelected > 1 && numRowsSelected < numRows: // More than 1 row selected
      opts = []
      break
    case numRowsSelected === numRows: // All rows selected
      opts = [5]
      break
    default: // Just in case
      opts = []
  }

  // Disable configured options
  $.each(opts, function (k, opt) {
    contextMenu.find('li').eq(opt).attr('class', 'disabled')
    contextMenu.find('li').eq(opt).find('a').prop('disabled', true)
  })
}

/**
 * Helper function to change state of selection buttons on events
 * @param {object} table - table object
 * @return {void}
 */
function handleSelectButtons (table) {
  if (table.rows('.selected').data().length === 0) {
    $('#selectAllDocs').prop('disabled', false)
    $('#deselectAllDocs').prop('disabled', true)
    $('#deleteSelectedDocs').prop('disabled', true)
  } else {
    $('#selectAllDocs').prop('disabled', false)
    $('#deselectAllDocs').prop('disabled', false)
    $('#deleteSelectedDocs').prop('disabled', false)
  }
}
