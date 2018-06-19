import * as utility from './utility.js'

/**
 * check all the easy error with js, in this case, you need more than 2 documents
 * @returns {string | null} the errors that is checked by JS, if there is no error the result will be null
 */
function submissionError () {
  const manageUrl = $('#manage-url').data().url
  const uploadUrl = $('#upload-url').data().url
  const activeFileNumTooFewErr = `You do not have enough active documents. 
  Please activate at least two documents using the <a href=${manageUrl}>Manage</a> tool 
  or <a href=${uploadUrl}>Upload</a> a new document.`
  if ($('#num_active_files').val() < 2) {
    return activeFileNumTooFewErr
  } else {
    return null
  }
}

/**
 * display the result of the similarity query on web page
 * @returns {void}
 */
function generateSimResult () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // the configuration for creating data table
  const dataTableConfig = {
    // do not display pages
    paging: false,

    // specify where the button is
    dom: `<'row'<'col-sm-6'l><'col-sm-6 text-right'B>>
          <'row'<'col-sm-12'tr>><'row'<'col-sm-4'i><'col-sm-8'p>>`,

    // specify all the button that is put on to the page
    buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5'],

    // Center all the data in the table.
    columnDefs: [
      {'className': 'text-center', 'targets': '_all'}
    ]
  }

  // send the ajax request
  utility.sendAjaxRequest('/similarityHTML', form)
    .done(
      function (response) {
        const outerTableDivSelector = $('#simTable')
        // put the response onto the web page
        outerTableDivSelector.html(response)
        // initialize the data table
        outerTableDivSelector.children().DataTable(dataTableConfig)
        // display the similarity result
        $('#similaritiesResults').css({'display': 'block'}) // display everything
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('error encountered while generating the similarity query result.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

$(function () {
  // hide the similarity
  $('#similaritiesResults').css({'display': 'none'})
  /**
   * The event handler for generate similarity clicked
   */
  $('#get-sims').click(function () {
    const error = submissionError() // the error happens during submission

    if (error === null) { // if there is no error
      generateSimResult()
    } else {
      utility.runModal(error)
    }
  })
})
