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
 * the function to run the error modal
 * @param {string} htmlMsg  - the message to display, you can put html in it
 * @returns {void} - this function returns nothing.
 */
function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * The function to create the ajax object
 * @param {object.<string, string>} form the form converted into a json
 * @returns {jquery.Ajax} - the jquery ajax object (a deferred object)
 */
function sendAjaxRequest (form) {
  return $.ajax({
    type: 'POST',
    url: '/dendrogramDiv',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(form)
  })
}

/**
 * the function to submit form via ajax in dendrogram
 * @returns {void} - nothing is returned from this function.
 */
function submitForm () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest(form)
    .done(
      function (response) {
        $('#dendrogram-result').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('error encountered while plotting the dendrogram.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

/**
 * the error message for the submission
 * @returns {string | null} - if it is null, it means no error, else then the string is the error message
 */
function submissionError () {
  const activeFileNumTooFewErr = 'A dendrogram requires at least 2 active documents to be created.'
  const activeFiles = $('#num_active_files').val()
  if (activeFiles < 2) {
    return activeFileNumTooFewErr
  } else {
    return null
  }
}

/**
 * When the HTML documents finish loading
 */
$(function () {
  /**
   * the events after dendrogram is clicked
   */
  $('#getdendro').on('click', function () {
    const error = submissionError() // the error happens during submission

    if (error === null) { // if there is no error
      submitForm()
    } else {
      runModal(error)
    }
  })
})
