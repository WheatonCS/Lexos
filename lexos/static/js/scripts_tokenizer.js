/**
 * the function to run the error modal
 * @param htmlMsg {string} - the message to display, you can put html in it
 */
function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * check all the easy error with js, in this case, you need more than 1 document
 * @returns {string | null} the errors that is checked by JS, if there is no error the result will be null
 */
function submissionError () {
  if ($('#num_active_files').val() < 1) {
    return 'You must have at least one active document to proceed!'
  } else {
    return null
  }
}

/**
 * the function to convert the form into json
 * @returns {{string: string}} - the form converted to json
 */
function jsonifyForm () {
  const form = {}
  $.each($('form').serializeArray(), function (i, field) {
    form[field.name] = field.value || ''
  })
  return form
}

/**
 * send the ajax request
 * @param url: the url to post
 * @param form: the form data packed into an object
 * @returns {jQuery.Ajax}: an jQuery Ajax object
 */
function sendAjaxRequest (url, form) {
  return $.ajax({
    type: 'POST',
    url: url,
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(form)
  })
}

function getDataTableConfig () {
  // Declare the variable that holds the number of fixed left columns.
  let numFixedColumns
  if ($('#table-orientation-column').is(':checked'))
    numFixedColumns = 3
  else if ($('#table-orientation-row').is(':checked'))
    numFixedColumns = 1

  return {
    scrollX: true,
    bSortCellsTop: true,
    // specify where the button is
    dom: `<'row'<'col-sm-6'l><'col-sm-6 text-right'B>>
              <'row'<'col-sm-12'tr>><'row'<'col-sm-4'i><'col-sm-8'p>>`,

    // specify all the button that is put on to the page
    buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5'],

    // Set number of fixed columns on left of the data table.
    fixedColumns: {
      leftColumns: numFixedColumns
    }
  }
}

function checkTokenizerSize () {
  // convert form into an object map string to string
  const form = jsonifyForm()

  sendAjaxRequest('/tokenizerSize', form)
    .done(
      function (response) {
        const size = Number(response)
        console.log(size)
        console.log("IN RESPONSE")
        if (size < 10000) {
          console.log("IN IF")
          generateTokenizerResult()
        } else {
          const outerTableDivSelector = $('#tokenizerMatrix')
          // put the response onto the web page
          outerTableDivSelector.html(response)
        }
      }
    )

    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('Error encountered while generating the lol result.')
      }
    )
}

/**
 * display the result of the similarity query on web page
 */
function generateTokenizerResult () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest('/tokenizerMatrix', form)
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
        runModal('Error encountered while generating the tokenize table result.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

$(function () {
  /**
   * The event handler for generate tokenize clicked.
   */
  $('#download-tokenizer').click(function (event) {
    // On check possible submission error on click.
    const error = submissionError()
    // If error found, run modal to display message and prevent the submission from happening.
    if (error !== null) {
      runModal(error)
      event.preventDefault()
    }
  })
  $('#get-tokenizer').click(function () {
    // Get the possible error happened during submission the ajax call.
    const error = submissionError()

    if (error === null) {  // If there is no error, do the ajax call.
      checkTokenizerSize()
    } else {               // If error found, do modal.
      runModal(error)
    }
  })
})
