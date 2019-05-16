import * as utility from './utility.js'

/**
 * Display the result of the tokenizer matrix on web page.
 * @returns {void}.
 */
function generateTokenizerResult () {
  const form = utility.jsonifyForm()
  // Send the ajax request to get the tokenizer matrix size.
  utility.sendAjaxRequest('/tokenizerHeader', form)
    .done(
      function (response) { $('#matrix').html(response) }
    )
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('Error encountered while calculating the size of the tokenizer result.')
      }
    )

  const numFixedColumns = $('#table-orientation-column').is(':checked') ? 3 : 1
  // convert form into an object map string to string
  $('#matrix').DataTable({
    // Below are appearance related settings.
    // Allow scroll horizontally.
    scrollX: true,
    // Do not sort headers.
    bSortCellsTop: true,
    // // specify where the button is
    // dom: `<'row'<'col-md-12 text-right'l>>
    //       <'row'<'col-md-6'B><'col-md-6 text-right'f>>
    //       <'row'<'col-md-12'tr>>
    //       <'row'<'col-md-5'i><'col-md-7'p>>`,

    // // specify all the button that is put on to the page
    // buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5', 'colvis'],

    // Set number of fixed columns on left of the data table.
    fixedColumns: {leftColumns: numFixedColumns},

    // Truncate the long words in most left column.
    columnDefs: [
      {
        targets: 0,
        render: $.fn.dataTable.render.ellipsis(15, true)
      }
    ],
    // Below are server processing related settings.
    processing: true,
    serverSide: true,
    ajax: {
      type: 'POST',
      url: '/tokenizerMatrix',
      contentType: 'application/json',
      data: function (data) {
        return JSON.stringify(
          Object.assign({}, data, utility.jsonifyForm())
        )
      }
    }
  })
}

$(function () {
  // The event handler for clicking on download matrix in the modal.
  $('#choose-download').click(function () {
    $('#download-tokenizer').click()
  })
  // The event handler for clicking on continue rendering in the modal.
  $('#choose-continue').click(function () {
    generateTokenizerResult()
  })

  // The event handler for download tokenize clicked.
  $('#download-tokenizer').click(function (download) {
    // On check possible submission error on click.
    const error = utility.submissionError(1)
    // If error found, run modal to display message and prevent the submission from happening.
    if (error !== null) {
      utility.runModal(error)
      download.preventDefault()
    }
  })

  // The event handler for generate tokenize clicked.
  $('#get-tokenizer').click(function () {
    // Get the possible error happened during submission the ajax call.
    const error = utility.submissionError(1)

    if (error === null) { // If there is no error, do the ajax call.
      generateTokenizerResult()
    } else { // If error found, do modal.
      utility.runModal(error)
    }
  })
})
