/**
 * The function to run the error modal.
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
