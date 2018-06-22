import * as utility from './utility.js'

/**
 * Get the data table configuration based on selected orientation.
 * @returns {{scrollX: boolean, bSortCellsTop: boolean, dom: string, buttons: string[], fixedColumns: {leftColumns: number}, columnDefs: *[]}}
 * The desired data table configuration.
 */
function getDataTableConfig () {
  // Declare the variable that holds the number of fixed left columns.
  const numFixedColumns = $('#table-orientation-column').is(':checked') ? 3 : 1

  return {
    // Allow scroll horizontally.
    scrollX: true,
    // Do not sort headers.
    bSortCellsTop: true,
    // specify where the button is
    dom: `<'row'<'col-sm-12 text-right'l>>
          <'row'<'col-sm-6'B><'col-sm-6 text-right'f>>
          <'row'<'col-sm-12'tr>>
          <'row'<'col-sm-6'i><'col-sm-7'p>>`,

    // specify all the button that is put on to the page
    buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5', 'colvis'],

    // Set number of fixed columns on left of the data table.
    fixedColumns: {
      leftColumns: numFixedColumns
    },

    // Truncate the long words in most left column.
    columnDefs: [
      {
        targets: 0,
        render: $.fn.dataTable.render.ellipsis(15, true)
      }
    ]
  }
}

/**
 * Check if the table is too large, if too large, give user the option to choose.
 * @returns {void}.
 */
function checkTokenizerSize () {
  // convert form into an object map string to string.
  const form = utility.jsonifyForm()
  // Send the ajax request to get the tokenizer matrix size.
  utility.sendAjaxRequest('/tokenizerSize', form)
    .done(
      function (response) {
        // Cast the response to an integer.
        const size = Number(response)
        if (size < 50000) { // If less than 50000 data, render the table.
          generateTokenizerResult()
        } else { // Else give user the option to download or keep waiting.
          $('#decision-button').click()
        }
      }
    )
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('Error encountered while calculating the size of the tokenizer result.')
      }
    )
}

/**
 * Display the result of the tokenizer matrix on web page.
 * @returns {void}.
 */
function generateTokenizerResult () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/tokenizerMatrix', form)
    .done(
      function (response) {
        const outerTableDivSelector = $('#tokenizerMatrix')
        // put the response onto the web page
        outerTableDivSelector.html(response)
        // initialize the data table
        outerTableDivSelector.children().DataTable(getDataTableConfig())
        // display everything in the tokenize div.
        $('#tokenizerResult').css({'display': 'block'})
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('Error encountered while generating the tokenize table result.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
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
      checkTokenizerSize()
    } else { // If error found, do modal.
      utility.runModal(error)
    }
  })
})
