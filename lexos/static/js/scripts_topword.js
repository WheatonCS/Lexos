/**
 * the function to run the error modal
 * @param {string} htmlMsg - the message to display, you can put html in it
 * @returns {void}
 */
function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * check all the easy error with js, in this case, you need more than 2 documents
 * @returns {string | null} the errors that is checked by JS, if there is no error the result will be null
 */
function submissionError () {
  if ($('#num_active_files').val() < 2) {
    return 'You must have at least 2 active documents to proceed!'
  } else {
    return null
  }
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
 * @param {string} url: the url to post
 * @param {object.<string, string>} form: the form data packed into an object
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
 * display the result of the top words on web page
 * @returns {void}
 */
function generateTopWordResult () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest('/topwordResult', form)
    .done(
      function (response) {
        const topWordHeader = $('#topword-header')
        const topWordResult = $('#topword-result')
        // Put the header in response to the legend.
        topWordHeader.html(response['header'])
        // Format each table and put them in the result div.
        topWordResult.html(response['results'].map(
          function (result) { return `<div class="row col-lg-6 col-md-6"><legend>${result["header"]}</legend>${result["result"]}</div>` }))
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('error encountered while generating the similarity query result.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

$(function () {
  // Hide unnecessary div for DTM
  $('#normalize-options').css({'visibility': 'hidden'})
  // set the normalize option to raw count
  $('#normalizeTypeRaw').attr('checked', true)

  /**
   * The event handler for generate similarity clicked
   */
  $('#get-topwords').click(function () {
    const error = submissionError() // the error happens during submission

    if (error === null) { // if there is no error
      generateTopWordResult()
    } else {
      runModal(error)
    }
  })
})
