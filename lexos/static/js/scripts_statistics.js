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
 * At least one document is required to run the stats.
 * @returns {string | null}: the errors that is checked by JS, if no error the result will be null.
 */
function submissionError () {
  if ($('#num_active_files').val() < 1) {
    return 'You must have at least 1 active documents to proceed!'
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
 * Format the ajax call response to HTML format string.
 * @param {object} response: a json format string.
 * @return {object}: a json formatted file report.
 */
function formatFileReportResponse (response) {
  // Extract constant result from response and put the result into a reasonable report sentence.
  const unit = response['unit']
  const mean = `Average document size is ${response['mean']} ${unit}.`
  const stdDeviation = `Standard deviation of documents is ${response['std_deviation']} ${unit}.`
  const IQR = `Inter quartile range of documents is ${response['inter_quartile_range']} ${unit}.`

  // Find if anomaly detected by standard error analysis.
  const noAnomalySe = response['anomaly_se_small'] === [] && response['anomaly_se_large'] === []
  // Pick appropriate result for standard error analysis.
  const anomalySeResult =
    noAnomalySe ? '<b>No</b> anomaly detected by standard error test.'
      : 'Anomaly <b>detected</b> by standard error test.' +
      response['anomaly_se_small'].map(
        function (file) { return `<p style="padding-left: 20px"><b>Small:</b> ${file}</p>` }) +
      response['anomaly_se_large'].map(
        function (file) { return `<p style="padding-left: 20px"><b>Large:</b> ${file}</p>` })

  // Find if anomaly detected by standard error analysis.
  const noAnomalyIqr = response['anomaly_iqr_small'] === [] && response['anomaly_iqr_large'] === []
  // Pick appropriate result for standard error analysis.
  const anomalyIqrResult =
    noAnomalyIqr ? '<b>No</b> anomaly detected by inter quartile range test.'
      : 'Anomaly <b>detected</b> by inter quartile range test.' +
      response['anomaly_iqr_small'].map(
        function (file) { return `<p style="padding-left: 20px"><b>Small:</b> ${file}</p>` }) +
      response['anomaly_iqr_large'].map(
        function (file) { return `<p style="padding-left: 20px"><b>Large:</b> ${file}</p>` })

  // Return the retracted information.
  return {
    'IQR': IQR,
    'mean': mean,
    'stdDeviation': stdDeviation,
    'anomalySeResult': anomalySeResult,
    'anomalyIqrResult': anomalyIqrResult
  }
}

/**
 * Display the result of the corpus statistics report on web.
 * @return {string}: formatted file report.
 */
function generateStatsFileReport () {
  $('#status-analyze').css({'visibility': 'visible'})
  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest('/corpusStatsReport', form)
    .done(
      function (response) {
        const formattedResult = formatFileReportResponse(response)
        $('#file-report-mean').html(formattedResult.mean)
        $('#file-report-std-deviation').html(formattedResult.stdDeviation)
        $('#file-report-IQR').html(formattedResult.IQR)
        $('#file-report-anomaly-se-result').html(formattedResult.anomalySeResult)
        $('#file-report-anomaly-iqr-result').html(formattedResult.anomalyIqrResult)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        // If fail hide the loading icon.
        $('#status-analyze').css({'visibility': 'hidden'})
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('Error encountered while generating the corpus statistics.')
      })
}

/**
 * Display the result of the box plot on web page.
 * @return {string}: formatted file report.
 */
function generateStatsBoxPlot () {
  $('#status-analyze').css({'visibility': 'visible'})
  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest('/corpusBoxPlot', form)
    .done(
      function (response) {
        $('#box-plot').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('Error encountered while generating the box plot.')
      })
}

/**
 * Display the result of the file statistics on web.
 * @return {string}: formatted file report.
 */
function generateStatsFileTable () {
  $('#status-analyze').css({'visibility': 'visible'})
  // convert form into an object map string to string
  const form = jsonifyForm()

  // the configuration for creating data table
  const dataTableConfig = {
    // Set the initial page length.
    pageLength: 10,

    // Replace entries to documents.
    language: {
      'lengthMenu': 'Display _MENU_ documents',
      'info': 'Showing _START_ to _END_ of _TOTAL_ documents'
    },

    // Specify where the button is.
    dom: `<'row'<'col-sm-6'l><'col-sm-6 text-right'B>>
          <'row'<'col-sm-12'tr>><'row'<'col-sm-6'i><'col-sm-6'p>>`,

    // Specify all the download buttons that are displayed on the page.
    buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5']
  }

  // send the ajax request
  sendAjaxRequest('/fileStatsTable', form)
    .done(
      function (response) {
        const outerTableDivSelector = $('#file-stats-table')
        // put the response onto the web page
        outerTableDivSelector.html(response)
        // initialize the data table
        outerTableDivSelector.children().DataTable(dataTableConfig)
        // display the corpus statistics result
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
      }
    )
}

$(function () {
  // Hide the stats result div.
  $('#file-stats-result').css({'display': 'none'})
  $('#corpus-stats-result').css({'display': 'none'})

  // Hide the normalize options and set it to raw count.
  $('#normalizeTypeRaw').attr('checked', true)
  $('#normalize-options').css({'visibility': 'hidden'})

  // Toggle file selection & reset the maximum number of documents when 'Toggle All' is clicked
  $('#allCheckBoxSelector').on('click', function () {
    if (this.checked) {
      $('.file-selector:not(:checked)').trigger('click')
      $('#cullnumber').attr('max', $('.file-selector:checked').length)
    } else {
      $('.file-selector:checked').trigger('click')
      $('#cullnumber').attr('max', '0')
    }
  })

  /**
   * The event handler for generate statistics clicked. Before generate
   * stats result, get number of active files and id of active files.
   */
  $('#get-stats').click(function () {
    // Get all the checked files.
    const checkedFiles = $('.eachFileCheck :checked')
    // Set a variable to store checked file ids.
    let activeFileIds = ''
    // Store checked file ids by putting a blank between each id.
    checkedFiles.each(function () {
      activeFileIds += `${$(this).val()} `
    })
    // Store the variable to input field.
    $('#active_file_ids').val(activeFileIds)
    // Store the number of active files.
    $('#num_active_files').val(checkedFiles.length)

    // Get the possible error during the submission.
    const error = submissionError()

    if (error === null) {
      // Get the file stats table.
      generateStatsFileTable()
      // Display the file result table.
      $('#file-stats-result').css({'display': 'block'})

      // Only get corpus info when there are more than one file.
      if (checkedFiles.length > 1) {
        // Get the corpus result.
        generateStatsFileReport()
        // Get the box plot.
        generateStatsBoxPlot()
        // Display the result.
        $('#corpus-stats-result').css({'display': 'block'})
      } else { // Else hide the corpus stats result div.
        $('#corpus-stats-result').css({'display': 'none'})
      }
    } else {
      runModal(error)
    }
  })
})
