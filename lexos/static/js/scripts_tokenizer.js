import * as utility from './utility.js'

/**
 * Display the result of the tokenizer matrix on web page.
 * @returns {void}.
 */
function generateTokenizerResult () {
  // Get the form in HTML as a JSON object.
  const form = utility.jsonifyForm()
  // Get the number of fixed columns based on the table orientation.
  const numFixedColumns = $('#table-orientation-column').is(':checked') ? 3 : 1

  // Send the ajax request to get the tokenizer result.
  utility.sendAjaxRequest('/tokenizerHeader', form)
    .done( // If the ajax call succeeded.
      function (response) {
        const matrix = $('#matrix')
        // Insert the table header in to the table.
        matrix.html(response)

        // Initialize the table as a DataTable.
        matrix.DataTable({
          // --- Below are appearance related settings. ---

          // Allow scroll horizontally.
          scrollX: true,

          // Do not sort headers.
          bSortCellsTop: true,

          // specify where the button is
          dom: `<'row'<'col-md-6'B><'col-md-6 text-right'f>>
          <'row'<'col-md-12'tr>>
          <'row'<'col-md-4'l><'col-md-8 text-right'p>>`,

          // Set the default ordering.
          order: [[2, "desc"]],

          // Set number of fixed columns on left of the data table.
          fixedColumns: {leftColumns: numFixedColumns},

          // specify all the button that is put on to the page
          buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5', 'colvis'],

          // Truncate the long words in most left column.
          columnDefs: [{
            targets: 0,
            render: $.fn.dataTable.render.ellipsis(15, true)
          }],

          // --- Below are server-side related settings. ---
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
    )
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('Error encountered while generating the tokenizer result.')
      }
    )

}

$(function () {
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
