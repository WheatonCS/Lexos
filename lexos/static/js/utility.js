/**
 * The function to run the error modal with input string.
 * @param {string} htmlMsg: the message to display.
 * @returns {void}.
 */
export function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * The function to convert the form into json.
 * @returns {{string: string}}: the form converted to json.
 */
export function jsonifyForm () {
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
export function sendAjaxRequest (url, form) {
  return $.ajax({
    type: 'POST',
    url: url,
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(form)
  })
}

/**
 * Check if the number of document uploaded meets the minimum number of file required to run the tool.
 * @param {number} numFileRequired: the minimum number of file required to run the tool.
 * @returns {string | null}: the errors that is checked by JS, if no error the result will be null.
 */
export function submissionError (numFileRequired) {
  // Get the url for upload and manage page.
  const uploadUrl = $('#upload-url').data().url
  const manageUrl = $('#manage-url').data().url

  // Set the error message
  const activeFileNumTooFewErr = `You do not have enough active documents. Please 
                                  activate at least ${numFileRequired} documents 
                                  using the <a href=${manageUrl}>Manage</a> tool 
                                  or <a href=${uploadUrl}>Upload</a> a new document.`

  // Get the number of active files.
  const activeFiles = $('#num-active-files').data().number

  // Check if minimum number of required files exists.
  if (activeFiles < numFileRequired) {
    return activeFileNumTooFewErr
  } else {
    return null
  }
}

/**
 * Scrolls the page to a given div.
 * @param {Object} div: The jquery selector of the div.
 * @returns {void}.
 */
export function scrollToDiv (div) {
  $('html, body').animate({scrollTop: div.offset().top}, 1000)
}
