import * as utility from './utility.js'

/**
 * Display the result of the tokenizer matrix on web page.
 * @returns {void}.
 */
function generateTokenizerResult () {
  // Select the matrix table.
  const matrix = $('#matrix')
  // Clear the data table content if the table exists.
  if ($.fn.DataTable.isDataTable(matrix)) matrix.DataTable().clear().destroy()

  // Get the form in HTML as a JSON object.
  const form = utility.jsonifyForm()

  // Send the ajax request to get the tokenizer result.
  utility.sendAjaxRequest('/tokenizerHeader', form)
    .done( // If the ajax call succeeded.
      function (response) {
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
          dom: 'Bftrip',

          // Set the default ordering.
          order: [[2, 'desc']],

          // Set number of fixed columns on left of the data table.
          fixedColumns: {leftColumns: 3},

          // specify all the button that is put on to the page
          buttons: [
            {extend: 'excelHtml5', title: 'Tokenizer Result'},
            {extend: 'csvHtml5', title: 'Tokenizer Result'},
            {extend: 'pdfHtml5', title: 'Tokenizer Result'},
            'colvis'
          ],

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
                // Combine the two json objects.
                Object.assign({}, data, utility.jsonifyForm())
              )
            }
          }
        })
      }
    )
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log(`textStatus: ${textStatus}`)
        console.log(`errorThrown: ${errorThrown}`)
        utility.runModal('Error encountered while generating the tokenizer result.')
      }
    )

}

$(function () {
  // The event handler for downloading file col tokenize clicked.
  $('#download_file_col').click(function (download) {
    // On check possible submission error on click.
    const error = utility.submissionError(1)

    // If error found, run modal to display message and prevent the submission from happening.
    if (error != null) {
      utility.runModal(error)
      download.preventDefault()
    } else {
      $('#orientation').val('file_col')
      $('#trigger_download').click()
    }
  })

    // The event handler for downloading file row tokenize clicked.
  $('#download_file_row').click(function (download) {
    // On check possible submission error on click.
    const error = utility.submissionError(1)

    // If error found, run modal to display message and prevent the submission from happening.
    if (error != null) {
      utility.runModal(error)
      download.preventDefault()
    } else {
      $('#orientation').val('file_row')
      $('#trigger_download').click()
    }
  })

  // The event handler for generate tokenize clicked.
  $('#get_tokenizer').click(function () {
    // Get the possible error happened during submission the ajax call.
    const error = utility.submissionError(1)

    if (error == null) { // If there is no error, do the ajax call.
      generateTokenizerResult()
    } else { // If error found, do modal.
      utility.runModal(error)
    }
  })
})
