/* #### INITIATE SCRIPTS ON $(DOCUMENT).READY() #### */
$(function () {
  initTable() //call the function to initiate the main table
  tableAction()
})
/* INITIATE MAIN DATATABLE */

//* Change the element name and test whether the table variable persists
function initTable () {
  return (table = $('#demo').DataTable({
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
      //				{width: "150", type: 'natural', targets: "_all"},
    ],
    order: [[1, 'asc']]
  }))
}

function tableAction () {
  registerColumn() // Draw the table column and make it searchable.

  /* Add all rows with .selected to the DataTables activeRows array
   It does not appear that this array needs to be maintained after
   initialisation, but the code to do so is commented out for de-bugging. */
  activeRows = []
  //$('tbody tr').each(function (index)
  $(table).find('tbody tr').each(function (index) {
    if ($(this).hasClass('selected')) {
      i = ':eq(' + index + ')'
      table.rows(i).select()
      activeRows.push($(this).attr('id'))
    }
    if (activeRows.length !== 0) {
      //download option appears on the top righ of the table
      $('#bttn-downloadSelectedDocs').show()
    }
  })

  $('.col-sm-5').append('<p style=\'display:inline; float:left; width:200px !important;\' id=\'name\'></p>')
  // Data tables active documents counter wasn't working.
  // I wrote a new way to do this. First, append an inline p tag to where the default counter used to be before I took it out
  // NOTE the p is cleared when going to a new page of the table. To fix this, datatables.js must be made local and changed.

  registerSelectEvents()
  // Area Select events callback
  $('#demo').DataTable()
    .on('select', function (e, dt, type, indexes) {
      if (type === 'row') {
        let data = $('#demo').DataTable().rows(indexes).data()[0]
      }
    })
    .on('deselect', function (e, dt, type, indexes) {
      if (type === 'row') {
        let data = $('#demo').DataTable().rows(indexes).data()
      }
    })

  // perform the different right click options on the document.
  tableDocumentActions()

  // When the save button is clicked, call the save function
  $('#save').click(function () {
    saveFunction()
  })
  // When the Delete Selected button is clicked, call the deletion function
  $('#delete').click(function () {
    selected_rows = table.rows({selected: true}).nodes().to$()
    deleteAllSelected(selected_rows)
  })

  // Trigger selection buttons
  $('#selectAllDocs').click(function () { selectAll() })
  $('#disableAllDocs').click(function () { deselectAll() })
  $('#deleteSelectedDocs').click(function () {
    selected_rows = table.rows({selected: true}).nodes().to$()
    deleteAllSelected(selected_rows)
  })
  // Remove the footer from alert modals when hidden
  $('#alert-modal').on('hidden.bs.modal', function (e) {
    $('#alert-modal .modal-footer').remove()
  })
}

/* #### ENABLE SEARCH AND ORDERING IN THE TABLE */
// allows the user to order the text in ascending or descending and search
// within the document.
function registerColumn () {
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

/* #### SELECT EVENTS #### */

// Handle select events
function registerSelectEvents () {
  table
    .on('select', function (e, dt, type, indexes) {
      // Get selected rows as a jQuery object
      const selected_rows = table.rows(indexes).nodes().to$()
      // Call the ajax function
      enableRows(selected_rows)
      handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
      $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have ' + table.rows('.selected').data().length + ' active document(s)'
      document.getElementById('name').innerHTML = table.rows('.selected').data().length + ' active documents' // add the correct counter text to the p
      $('#bttn-downloadSelectedDocs').show()
    })
    .on('deselect', function (e, dt, type, indexes) {
      // Get deselected rows as a jQuery object
      const deselected_rows = table.rows(indexes).nodes().to$()
      // Call the ajax function
      disableRows(deselected_rows)
      handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
      document.getElementById('name').innerHTML = table.rows('.selected').data().length + ' active documents' // same as the other one
      $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have ' + table.rows('.selected').data().length + ' active document(s)'
      if (table.rows('.selected').data().length === 0) {
        $('#bttn-downloadSelectedDocs').hide()
      }
    })
}

/* #### DEFINE CONTEXT MENU #### */

/*Right click options on the documents*/
function tableDocumentActions () {
  // Get the number of rows, selected or unselected, for context menu
  const num_rows = table.rows().ids().length
  const num_rows_selected = table.rows({selected: true}).ids().length
  handleSelectButtons(num_rows, num_rows_selected)

  $('#demo').contextmenu({
    target: '#context-menu',
    scopes: 'td',
    before: function () {
      prepareContextMenu()
    },
    onItem: function (cell, e) {
      var target = cell.parent().attr('id')
      action = $(e.target).attr('data-context')
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
          deleteDoc(target)
          break
        case 'select_all':
          selectAll()
          break
        case 'deselect_all':
          deselectAll()
          break
        case 'merge_selected':
          selected_rows = table.rows({selected: true}).nodes().to$()
          mergeSelected(cell, selected_rows)
          break
        case 'apply_class_selected':
          selected_rows = table.rows({selected: true}).nodes().to$()
          applyClassSelected(cell, selected_rows)
          break
        case 'delete_all_selected':
          selected_rows = table.rows({selected: true}).nodes().to$()
          deleteAllSelected(selected_rows)
          break
      }
    }
  })
  // Refresh context menu on show
  $('#context-menu').on('show.bs.context', function () {
    prepareContextMenu()
  })
}

/* #### SAVE BUTTON #### */

/*'save' button for the right click options on the document.*/
function saveFunction () {
  const merge = $('#merge').val()
  let row_id = $('#tmp-row').val()
  const column = $('#tmp-column').val()
  const value = $('#tmp').val()
  if (row_id.match(/,/)) {
    row_ids = row_id.split(',')
    source = $('#' + row_id).children().eq(3).text()
    if (merge === 'true') {
      if ($('#addMilestone').prop('checked') === true) {
        milestone = $('#milestone').val()
      } else {
        milestone = ''
      }
      mergeDocuments(row_ids, column, source, value, milestone)
    } else {
      saveMultiple(row_ids, column, value)
    }
  } else {
    saveOne(row_id, column, value)
  }
}

// Handle the milestone checkbox in the document merge modal
$(document).on('change', $('#addMilestone'), function () {
  $('#milestoneField').toggle()
})

/*------------------------*/
/*  SUPPORTING FUNCTIONS */
/*------------------------*/

/*  toggleActiveDocsIcon() */

// Shows or hides the Active Documents icon in response to the table state
function toggleActiveDocsIcon () {
  // Hide the active docs icon if there are no docs selected
  if (table.rows({selected: true}).ids().length < 1) {
    $('.fa-folder-open-o').fadeOut(200)
  } else {
    $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have ' + table.rows({selected: true}).ids().length + ' active document(s)'
    $('.fa-folder-open-o').fadeIn(200)
  }
}

/* #### selectAll() #### */

// Sets the selected status of all documents in the File Manager and UI to selected.
function selectAll () {
  sendAjaxRequestSelectAll('/selectAll')
    .done(
      function (response) {
        // Select All Rows in the UI
        table.rows().select()
        handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
        toggleActiveDocsIcon()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not select all the documents.')
        $('#error-modal').modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

function sendAjaxRequestSelectAll (url) {
  return $.ajax({
    type: 'POST',
    url: url
  })
}

/* #### deselectAll() #### */

// Sets the selected status of all documents in the File Manager and UI to deselected.
function deselectAll () {
  sendAjaxRequestDeselect('/deselectAll')
    .done(
      function (response) {
        // Deselect All Rows in the UI
        table.rows().deselect()
        handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
        toggleActiveDocsIcon()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not deselect all the documents.')
        $('#error-modal').modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

function sendAjaxRequestDeselect (url) {
  return $.ajax({
    type: 'POST',
    url: url
  })
}

/* #### enableRows() #### */

// Enables selected rows in the File Manager and sets UI to selected.
function enableRows (selected_rows) {
  var file_ids = []
  selected_rows.each(function (index) {
    file_ids.push($(this).attr('id'))
  })
  // Ensure file_ids contains unique entries
  file_ids = unique(file_ids)
  // Convert the file_ids list to a json string for sending
  const data = JSON.stringify(file_ids)

  sendAjaxRequestEnableRows('enableRows', data)
    .done(function (response) {
      handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
      toggleActiveDocsIcon()
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      $('#error-modal .modal-body').html('Lexos could not select the requested documents.')
      $('#error-modal').modal()
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    })
}

function sendAjaxRequestEnableRows (url, data) {
  return $.ajax({
    type: 'POST',
    url: '/enableRows',
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/* #### disableRows() #### */

// Disables selected rows in the File Manager and sets UI to deselected.
function disableRows (deselected_rows) {
  var file_ids = []
  deselected_rows.each(function (index) {
    file_ids.push($(this).attr('id'))
  })
  // Ensure file_ids contains unique entries
  file_ids = unique(file_ids)
  // Convert the file_ids list to a json string for sending
  const data = JSON.stringify(file_ids)
  sendAjaxRequestDisableRow('/disableRows', data)
    .done(
      function (response) {
        handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
        toggleActiveDocsIcon()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not deselect the requested documents.')
        $('#error-modal').modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

function sendAjaxRequestDisableRow (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })

}

/* #### showPreviewText() #### */

//* Opens modal containing the document preview text.
function showPreviewText (row_id) {
  sendAjaxRequestPreview('/getPreview', row_id)
    .done(
      function (response) {
        response = JSON.parse(response)
        const title = 'Preview of <b>' + response['label'] + '</b>'
        var text = response['previewText']
        // Encode tags as HTML entities
        text = String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
        //* To Do: Convert tagged texts to strings
        $('.modal-title').html(title)
        $('#preview_text').html(text)
        $('#preview').modal()
      })
    .fail(function (jqXHR, textStatus, errorThrown) {
      $('#error-modal .modal-body').html('Lexos could not retrieve the file preview.')
      $('#error-modal').modal()
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    })
}

function sendAjaxRequestPreview (url, row_id) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: row_id,
    contentType: 'charset=UTF-8'
  })
}

/* #### editName() #### */
function editName (row_id) {
  $('#edit-form').remove()
  cell_name = $('#' + row_id).find('td:eq(1)').text()
  var form = '<div id="edit-form">Document Name <input id="tmp" type="text" value="' + cell_name + '">'
  form += '<input id="tmp-row" type="hidden" value="' + row_id + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="1"></div>'
  $('#edit_title').html('Edit Name of <b>' + cell_name + '</b>')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/* #### editClass() #### */
function editClass (row_id) {
  $('#edit-form').remove()
  doc_name = $('#' + row_id).find('td:eq(1)').text()
  cell_value = $('#' + row_id).find('td:eq(2)').text()
  var form = '<div id="edit-form">Class Label <input id="tmp" type="text" value="' + cell_value + '">'
  form += '<input id="tmp-row" type="hidden" value="' + row_id + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="2"></div>'
  $('#edit_title').html('Edit <b>' + doc_name + '</b> Class')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/* #### mergeSelected() #### */
function mergeSelected (cell, selected_rows) {
  row_ids = []
  selected_rows.each(function () {
    id = $(this).attr('id')
    row_ids.push(id)
  })
  $('#edit-form').remove()
  cell_value = 'merge-' + $('#' + row_ids[0]).find('td:eq(1)').text()
  var form = '<div id="edit-form">New Document Name '
  form += '<input id="tmp" type="text" value="' + cell_value + '"><br>'
  form += '<input id="addMilestone" type="checkbox"> Add milestone at end of documents'
  form += '<span id="milestoneField" style="display:none;">'
  form += '<br>Milestone <input id="milestone" type="text" value="#EOF#"></span>'
  form += '<input id="merge" type="hidden" value="true">'
  form += '<input id="tmp-row" type="hidden" value="' + row_ids + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="2"></div>'
  $('#edit_title').html('Merge Selected Documents')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/* #### applyClassSelected() #### */
function applyClassSelected (cell, selected_rows) {
  row_ids = []
  selected_rows.each(function () {
    id = $(this).attr('id')
    row_ids.push(id)
  })
  $('#edit-form').remove()
  cell_value = cell.text()
  var form = '<div id="edit-form">Class Label <input id="tmp" type="text" value="' + cell_value + '">'
  form += '<input id="tmp-row" type="hidden" value="' + row_ids + '"></div>'
  form += '<input id="tmp-column" type="hidden" value="2"></div>'
  $('#edit_title').html('Apply <b>' + cell_value + '</b> Class to Selected Documents')
  $('#modal-body').html(form)
  $('#edit-modal').modal()
}

/* #### mergeDocuments() #### */

// Helper function saves value in edit dialog and updates table with a new document
function mergeDocuments (row_ids, column, source, value, milestone) {
  // Validation - make sure the document name is not left blank
  if (value == '') {
    msg = '<p>A document without a name is like coffee without caffeine!</p><br>'
    msg += '<p>Make sure you don\'t leave the New Document Name field blank.</p>'
    $('#alert-modal .modal-body').html(msg)
    $('#alert-modal').modal()
    return false
  }

  // Prepare data and request
  url = '/mergeDocuments'
  data = JSON.stringify([row_ids, value, source, milestone])

  // Do Ajax
  sendAjaxRequestMergedocuments(url, data)
    .done(
      function (response) {
        var table = $('#demo').DataTable()
        response = JSON.parse(response)
        var newIndex = response[0]
        // var newIndex = parseInt(row_ids.slice(-1)[0])+1;
        table.rows().deselect()
        text = response[1].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
        var rowNode = table.row
          .add([newIndex, value, '', source, text])
          .draw(false)
          .node()
        table.rows(newIndex).select() // This automatically calls enableRows()
        $(rowNode)
          .attr('id', newIndex)
          .addClass('selected')
        $(rowNode).children().first().css('text-align', 'right')
        handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
        $('.fa-folder-open-o')[0].dataset.originalTitle = 'You have 1 active document(s)'
        // toggleActiveDocsIcon();
        $('#edit-modal').modal('hide')
        $('#edit-form').remove()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not merge the requested documents or could not save the merged document.')
        $('#error-modal').modal()
        $('#edit-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

function sendAjaxRequestMergedocuments (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/* #### saveMultiple() #### */

// Helper function saves value in edit dialog and updates table for multiple rows
function saveMultiple (row_ids, column, value) {
  // Prepare data and request
  url = '/setClassSelected'
  data = JSON.stringify([row_ids, value])
  // Do Ajax
  sendAjaxRequestSaveMultiple(url, data)
    .done(
      function (response) {
        row_ids = JSON.parse(response)
        // Update the UI
        var reloadPage = false
        $.each(row_ids, function (i) {
          id = '#' + row_ids[i]
          $(id).find('td:eq(2)').text(value)
          if ($(id).length == 0) {
            reloadPage = true
          }
        })
        $('#edit-modal').modal('hide')
        $('#edit-form').remove()
        // Ugly hack to make sure rows are updated across table pages
        if (reloadPage == true) {
          window.location.reload()
        } else {
          toggleActiveDocsIcon()
          table.draw()
        }
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not update the class of the requested documents.')
        $('#error-modal').modal()
        $('#delete-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })

}

function sendAjaxRequestSaveMultiple (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/* #### saveOne() #### */

// Helper function saves value in edit dialog and updates table
function saveOne (row_id, column, value) {
  // Validation - make sure the document name is not left blank
  if (column == 1 && value == '') {
    msg = '<p>A document without a name is like coffee without caffeine!</p><br>'
    msg += '<p>Make sure you don\'t leave the field blank.</p>'
    $('#alert-modal .modal-body').html(msg)
    $('#alert-modal').modal()
    revert = $('#' + row_id).find('td:eq(1)').text()
    $('#tmp').val(revert)
    return false
  }
  // Prepare data and request
  data = JSON.stringify([row_id, value])
  url = ''
  switch (column) {
    case '1':
      url = '/setLabel'
      err_msg = 'Lexos could not update the document name.'
      break
    case '2':
      url = '/setClass'
      err_msg = 'Lexos could not update the document class.'
      break
  }
  sendAjaxRequestSaveOne(url, data)
    .done(
      function (response) {
        // Update the UI
        cell = 'td:eq(' + column + ')'
        $('#' + row_id).find(cell).text(value)
        $('#edit-modal').modal('hide')
        $('#edit-form').remove()
        table.draw()
        toggleActiveDocsIcon()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html(err_msg)
        $('#error-modal').modal()
        $('#edit-form').remove()
        $('#edit-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

function sendAjaxRequestSaveOne (url, data) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: data,
    contentType: 'application/json;charset=UTF-8',
    cache: false
  })
}

/* #### deleteOne() #### */

// Helper function deletes selected row and updates table
function deleteOne (row_id) {
  // alert("Delete: " + row_id);
  url = '/deleteOne'

  sendAjaxRequestDeleteOne(url, row_id)
    .done(
      function (response) {
        // Update the UI
        id = '#' + row_id
        table.row(id).remove()
        handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
        toggleActiveDocsIcon()
        table.draw()
      })
    .fail(function (jqXHR, textStatus, errorThrown) {
      $('#error-modal .modal-body').html('Lexos could not delete the requested document.')
      $('#error-modal').modal()
      $('#delete-modal').modal('hide')
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    })
}

function sendAjaxRequestDeleteOne (url, row_id) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: row_id,
    contentType: 'charset=UTF-8',
    cache: false
  })

}

/* #### deleteDoc() #### */

// deletes the selected document or the document where the user right clicks
function deleteDoc (row_id) {
  doc_name = $('#' + row_id).find('td:eq(1)').text()
  html = '<p>Are you sure you wish to delete <b>' + doc_name + '</b>?</p>'
  html += '<span id="deleteId" style="display:none;">' + row_id + '</span>'
  footer = '<div class="modal-footer"><button type="button" data-dismiss="modal" class="btn btn-primary" id="confirm-delete-bttn" style="margin-left:2px;margin-right:2px;">Delete</button><button type="button" data-dismiss="modal" class="btn" style="margin-left:2px;margin-right:2px;">Cancel</button></div>'
  $('#delete-modal .modal-body').html(html)
  $('#delete-modal .modal-body').append(footer)
  $('#delete-modal').modal()
    .one('click', '#confirm-delete-bttn', function () {
      row_id = $('#deleteId').text()
      deleteOne(row_id)
    })
}

/* #### deleteSelected() #### */

// Helper function deletes selected rows and updates table
function deleteSelected (row_ids) {
  url = '/deleteSelected'

  // Do Ajax
  sendajaxRequestDeleteSelected(url, row_ids)
    .done(
      function (response) {
        // Update the UI
        row_ids = JSON.parse(response)
        // row_ids = row_ids.split(",");
        $.each(row_ids, function (i) {
          id = '#' + row_ids[i]
          table.row(id).remove()
        })
        handleSelectButtons(table.rows().ids().length, table.rows({selected: true}).ids().length)
        toggleActiveDocsIcon()
        table.draw()
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not delete the requested documents.')
        $('#error-modal').modal()
        $('#delete-modal').modal('hide')
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      })
}

function sendajaxRequestDeleteSelected (url, row_ids) {
  return $.ajax({
    type: 'POST',
    url: url,
    data: row_ids,
    contentType: 'charset=UTF-8',
    cache: false
  })
}

/* #### deleteAllSelected() #### */
function deleteAllSelected (selected_rows) {
  row_ids = []
  selected_rows.each(function () {
    id = $(this).attr('id')
    row_ids.push(id)
  })
  html = '<p>Are you sure you wish to delete the selected documents?</p>'
  html += '<span id="deleteIds" style="display:none;">' + row_ids.toString() + '</span>'
  footer = '<div class="modal-footer"><button type="button" data-dismiss="modal" class="btn btn-primary" id="confirm-delete-bttn" style="margin-left:2px;margin-right:2px;">Delete</button><button type="button" data-dismiss="modal" class="btn" style="margin-left:2px;margin-right:2px;">Cancel</button></div>'
  $('#delete-modal .modal-body').html(html)
  $('#delete-modal .modal-body').append(footer)
  $('#delete-modal').modal()
    .one('click', '#confirm-delete-bttn', function () {
      row_ids = $('#deleteIds').text()
      deleteSelected(row_ids)
    })
}

/* #### unique() #### */

// Helper function ensures id lists have no duplicates
function unique (array) {
  return $.grep(array, function (el, index) {
    return index === $.inArray(el, array)
  })
}

/* #### prepareContextMenu() #### */
// Helper function to change configure the context menu based on
// the number of rows currently selected

function prepareContextMenu () {
  // Refresh all options
  $('#context-menu').find('li').removeClass('disabled')
  $('#context-menu').find('li').find('a').removeProp('disabled')

  // Comparison values
  num_rows = table.rows().ids().length
  num_rows_selected = table.rows({selected: true}).ids().length

  // Set config options -- Numbers refer to li elements, including dividers
  // The numbers below corresponds to the different options in right lick
  // on the document.
  switch (true) {
    /*  5: 'Select All Documents'
        6: 'Deselect All Documents
        8: 'Merge Selected Documents'
        9: 'Apply Class to Selected Documents'
        10: 'Delete Selected Documents'
    */
    case num_rows_selected === 0: // No rows selected
      opts = [6, 8, 9, 10]
      break
    case num_rows_selected === 1: // 1 row selected
      opts = [8, 9]
      break
    case num_rows_selected > 1 && num_rows_selected < num_rows: // More than 1 row selected
      opts = []
      break
    case num_rows_selected === num_rows: // All rows selected
      opts = [5]
      break
    default: // Just in case
      opts = []
  }

  // Disable configured options
  $.each(opts, function (k, opt) {
    $('#context-menu').find('li').eq(opt).attr('class', 'disabled')
    $('#context-menu').find('li').eq(opt).find('a').prop('disabled', true)
  })
}

/* #### handleSelectButtons() #### */

// Helper function to change state of selection buttons on events
function handleSelectButtons (num_rows, num_rows_selected) {
  if (table.rows('.selected').data().length === 0) {
    $('#selectAllDocs').prop('disabled', false)
    // $("#disableAllDocs").prop("disabled", true);
    $('#deleteSelectedDocs').prop('disabled', true)
  } else {
    if (table.rows('.selected').data().length === num_rows) {
      $('#selectAllDocs').prop('disabled', true)
      $('#disableAllDocs').prop('disabled', false)
      $('#deleteSelectedDocs').prop('disabled', false)
    } else {
      $('#selectAllDocs').prop('disabled', false)
      $('#disableAllDocs').prop('disabled', false)
      $('#deleteSelectedDocs').prop('disabled', false)
    }
  }
}
