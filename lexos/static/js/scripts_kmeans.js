import * as utility from './utility.js'

/**
 * Convert HTML table to data table with desired configurations.
 * @param {string} table: A HTML formatted table.
 * @returns {void}.
 */
function convertToDataTable (table) {
  const hideColumns =
    $('#vizMethod').val() === '3DScatter' ? [2, 3, 4] : [2, 3]

  table.DataTable({
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
        targets: hideColumns,
        visible: false,
        searchable: false
      }
    ]
  })
}

/**
 * Display the K-Means clustering result as a table on web though an Ajax call.
 * @returns {void}.
 */
function generateKMeansResult () {
  $('#status-analyze').css({'visibility': 'visible'})
  // Convert form into an object map string to string
  const form = utility.jsonifyForm()

  // Send the ajax request
  utility.sendAjaxRequest('/KMeansResult', form)
    .done(
      function (response) {
        // Insert the table result.
        const tableDiv = $('#KMeans-table')
        tableDiv.html(response['table'])
        // Change the HTML table to a data table.
        convertToDataTable(tableDiv.children())
        // Insert the plot result.
        $('#KMeans-plot').html(response['plot'])
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        // If fail hide the loading icon.
        $('#status-analyze').css({'visibility': 'hidden'})
        console.log(`textStatus: ${textStatus}`)
        console.log(`errorThrown: ${errorThrown}`)
        utility.runModal('Error encountered while generating the K-Means result.')
      })
    .always(
      function () {
        // Always hide the loading icon.
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

/**
 * Scrolls to the graph once its generated.
 * @returns {void}
 */
function scrollToGraph () {
  $('html, body').animate({
    scrollTop: $('#get-k-means-result').offset().top
  }, 1000)
}

$(function () {
  // Hide the K-Means result div when first get to the page.
  $('#KMeans-result').css({'display': 'none'})

  // The event handler when generate K-Means result is clicked.
  $('#get-k-means-result').click(function () {
    // Catch the possible error during submission.
    const error = utility.submissionError(2)

    if (error === null) {
      // If there is no error, get the result.
      $('#KMeans-result').css({'display': 'block'})
      generateKMeansResult()
      scrollToGraph()
    } else {
      utility.runModal(error)
    }
  })
})
