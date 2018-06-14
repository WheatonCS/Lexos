/**
 * the function to run the error modal
 * @param htmlMsg {string} - the message to display, you can put html in it
 */
function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * check all the easy error with js, in this case, one document is required
 * @returns {string | null} the errors that is checked by JS, if there is no error the result will be null
 */
function submissionError () {
  if ($('#num_active_files').val() < 3)
    return 'You must have at least 2 active documents to proceed!'
  else
    return null
}

/**
 * the function to convert the from into json
 * @returns {{string: string}} - the from converted to json
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

/**
 * display the table of the k means result on web.
 */
function generateKMeansTable () {
  $('#status-analyze').css({'visibility': 'visible'})
  // convert form into an object map string to string
  const form = jsonifyForm()

  // the configuration for creating data table
  const dataTableConfig = {
    // Do not paging.
    paging: false,
    // Set the Scroll Height.
    scrollY: 300,
    // If not enough height, shrink the table height.
    scrollCollapse: true,
    // Specify where the button is.
    dom: `<'row'<'col-sm-12 text-right'f>><'row'<'col-sm-12 'tr>><'row'<'col-sm-12 text-right'B>>`,
    // Specify all the download buttons that are displayed on the page.
    buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5'],
    // Truncate long documentation names.
    columnDefs: [{
      targets: 1,
      render: $.fn.dataTable.render.ellipsis(15, true)
    }]
  }

  // send the ajax request
  sendAjaxRequest('/KMeansTable', form)
    .done(
      function (response) {
        const outerTableDivSelector = $('#KMeans-table')
        // put the response onto the web page
        outerTableDivSelector.html(response)
        // initialize the data table
        outerTableDivSelector.children().DataTable(dataTableConfig)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        // If fail hide the loading icon.
        $('#status-analyze').css({'visibility': 'hidden'})
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('Error encountered while generating the file statistics.')
      })
}

/**
 * display the result of the box plot on web page
 */
function generateKMeansPlot () {
  $('#status-analyze').css({'visibility': 'visible'})
  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest('/KMeansPlot', form)
    .done(
      function (response) {
        $('#KMeans-plot').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('Error encountered while generating the box plot.')
      })
    .always(
      function () {
        // Always hide the loading icon.
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

$(function () {
  // Hide the K-Means result div when first get to the page.
  $('#KMeans-result').css({'display': 'none'})

  /**
   * The event handler for generate statistics clicked.
   */
  $('#get-k-means-result').click(function () {
    // the error happens during submission
    const error = submissionError()

    if (error === null) {  // if there is no error
      // Get the file report result.
      $('#KMeans-result').css({'display': 'block'})
      generateKMeansTable()
      generateKMeansPlot()

    }
    else {
      runModal(error)
    }
  })
})

