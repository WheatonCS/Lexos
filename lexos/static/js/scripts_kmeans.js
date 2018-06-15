/**
 * The function to run the error modal.
 * @param {string} htmlMsg: the message to display.
 * @returns {void}.
 */
function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * At least two documents are required to run the K-Means clustering.
 * @returns {string | null}: the errors that is checked by JS, if no error the result will be null.
 */
function submissionError () {
  if ($('#num_active_files').val() < 3) {
    return 'You must have at least 2 active documents to proceed!'
  } else {
    return null
  }
}

/**
 * The function to convert the form into json.
 * @returns {{string: string}}: the form converted to json.
 */
function jsonifyForm () {
  const form = {}
  $.each($('form').serializeArray(), function (i, field) {
    form[field.name] = field.value || ''
  })
  return form
}

/**
 * Send the ajax request.
 * @param {string} url: the url to post.
 * @param {{string: string}} form: the form data packed into an object.
 * @returns {jQuery.Ajax}: an jQuery Ajax object.
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
 * Return the desired data table configuration.
 * @returns {{paging: boolean, scrollY: number, scrollCollapse: boolean, dom: string, buttons: string[], columnDefs: *[]}}
 */
function getDataTableConfiguration () {
  const hide_columns =
    $('#vizMethod').val() === '3DScatter' ? [2, 3, 4] : [2, 3]

  return {
    // Do not paging.
    paging: false,
    // Set the Scroll Height.
    scrollY: 300,
    // If not enough height, shrink the table height.
    scrollCollapse: true,
    // Specify where the button is.
    dom: `<'row'<'col-sm-12 text-right'f>>
          <'row'<'col-sm-12 'tr>>
          <'row k-means-result-download-button'<'col-sm-12'B>>`,
    // Specify all the download buttons that are displayed on the page.
    buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5'],

    columnDefs: [
      { // Truncate long documentation names.
        targets: 1,
        render: $.fn.dataTable.render.ellipsis(15, true)
      },
      { // Hide columns which hold the coordinates.
        targets: hide_columns,
        visible: false,
        searchable: false
      }
    ]
  }
}

/**
 * Display the K-Means clustering result as a table on web though an Ajax call.
 * @returns {void}.
 */
function generateKMeansResult () {
  $('#status-analyze').css({'visibility': 'visible'})
  // Convert form into an object map string to string
  const form = jsonifyForm()

  // Send the ajax request
  sendAjaxRequest('/KMeansResult', form)
    .done(
      function (response) {
        // Insert the table result.
        const tableDiv = $('#KMeans-table')
        tableDiv.html(response['table'])
        // Change the HTML table to a data table with desired configurations.
        tableDiv.children().DataTable(getDataTableConfiguration())
        // Insert the plot result.
        $('#KMeans-plot').html(response['plot'])
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        // If fail hide the loading icon.
        $('#status-analyze').css({'visibility': 'hidden'})
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('Error encountered while generating the file statistics.')
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

  // The event handler when generate K-Means result is clicked.
  $('#get-k-means-result').click(function () {
    // Catch the possible error during submission.
    const error = submissionError()

    if (error === null) {
      // If there is no error, get the result.
      $('#KMeans-result').css({'display': 'block'})
      generateKMeansResult()
    } else {
      runModal(error)
    }
  })
})
