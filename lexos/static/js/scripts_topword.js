/**
 * the function to run the error modal
 * @param {string} htmlMsg - the message to display, you can put html in it
 * @returns {void}.
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
  const manageUrl = $('#manage-url').data().url
  const uploadUrl = $('#upload-url').data().url
  const activeFileNumTooFewErr = `You do not have enough active documents. 
                                  Please activate at least two documents using 
                                  the <a href=${manageUrl}>Manage</a> tool or 
                                  <a href=${uploadUrl}>Upload</a> a new document.`
  if ($('#num-active-files').data().number < 2) {
    return activeFileNumTooFewErr
  } else {
    return null
  }
}

/**
 * Check if allow comparison among classes or classes to corpus.
 * @returns {void}.
 */
function checkAllowClassComparison () {
  const enableClassComparison = $('#num-active-classes').data().number < 2
  $('#classToPara').attr('disabled', enableClassComparison)
  $('#classToClass').attr('disabled', enableClassComparison)

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
 * Format json result into a more readable HTML format.
 * @param {object.<string, string>} result: contains result title and contents.
 * @returns {string}: A HTML formatted DIV contains result title and contents.
 */
function format (result) {
  return `<div class="topword-result col-lg-6 col-md-6">
              <fieldset class="row col-lg-12 col-md-12">
                  <legend id= "topwordTableTitle" style="font-size: 16px">${result['title']}</legend>
              </fieldset>
              <div class="row col-lg-12 col-md-12">
                  ${result['result']}
              </div>
          </div>`
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
        const topWordHeader = $('#topword-title')
        const topWordResult = $('#topword-result')
        // Put the header in response to the legend.
        topWordHeader.html(response['header'])
        // Format each table and put them in the result div.
        topWordResult.html(response['results'].map(
          function (result) { return format(result) }))
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
  // Hide unnecessary div for DTM.
  $('#normalize-options').css({'visibility': 'hidden'})
  // set the normalize option to raw count.
  $('#normalizeTypeRaw').attr('checked', true)
  // Check if comparison among classes should be enabled.
  checkAllowClassComparison()
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

