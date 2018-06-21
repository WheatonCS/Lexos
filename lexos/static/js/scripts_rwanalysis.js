/**
 * Show the milestone input when the milestone check box is checked.
 */
function updateMSopt () {
  if ($('#rollinghasmilestone').is(':checked')) {
    $('#rollingmilestoneopt').show()
  } else {
    $('#rollingmilestoneopt').hide()
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
 * the function to run the error modal
 * @param htmlMsg {string} - the message to display, you can put html in it
 */
function runModal (htmlMsg) {
  $('#error-modal-message').html(htmlMsg)
  $('#error-modal').modal()
}

/**
 * The function to create the ajax object
 * @param form {object.<string, string>} the form converted into a json
 * @returns {jquery.Ajax} - the jquery ajax object (a deferred object)
 */
function sendAjaxRequest (form) {

  return $.ajax({
    type: 'POST',
    url: '/rollingWindowGraph',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(form)
  })

}

/**
 * the function to submit form via ajax in dendrogram
 */
function submitForm () {
  // show loading icon
  $('#status-visualize').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = jsonifyForm()

  // send the ajax request
  sendAjaxRequest(form)
    .done(
      function (response) {
        $('#rwa-result-graph').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        runModal('error encountered while plotting the rolling window analysis.')
      })
    .always(
      function () {
        $('#status-visualize').css({'visibility': 'hidden'})
      })
}

function getSubmissionError () {
  // get the number of active document
  const numActiveDoc = Number($('#num_active_files').val())

  // if there is no active document
  if (numActiveDoc === 0)
    return 'Please select a document to analyze.'
  // no search pattern and window size
  else if ($('#rollingwindowsize').val() === '' || $('#rollingsearchword').val() === '')
    return 'Please fill out the \'Search Pattern(s)\' and \'Size of Rolling Window\' fields.'
  // cannot search term using window of chars
  else if ($('#inputword').prop('checked') && $('#windowletter').prop('checked'))
    return 'You cannot use tokens for search terms when analyzing a window of characters. ' +
      'The window setting has been changed to a window of tokens.'
  // no error found
  else
    return null
}

/* document.ready() Functions */
$(function () {

  // Call update milestone on page load
  updateMSopt()
  // Bind the function to the checkbox
  $('#rollinghasmilestone').click(updateMSopt)

  $('#getgraph').click(function () {
    /* Validation */
    const errorString = getSubmissionError()
    if (errorString === null)  // no error found
      submitForm()
    else
      runModal(errorString)
  })

  /* On-Click Validation */
  $('#radiowindowletter').click(function () {
    if ($('#inputword').prop('checked')) {
      $('#windowword').click()
      const msg = 'You cannot use a window of characters when analyzing a token.' +
        ' The setting has been changed to a window of tokens.'
      $('#error-modal-message').html(msg)
      $('#error-modal').modal()
    }
  })

  /* Other UI functionality */

  // Fixes bug where you cannot click second text box in firefox
  $('#rollingsearchwordopt, #rollingsearchword').hover(function () {
    $(this).focus()
  })

  // Sets the value of the hidden input
  $('.minifilepreview').click(function () {
    $('#filetorollinganalyze').val($(this).prop('id'))
  })

  // Shows the second textbox when rolling ratio gets clicked
  $('#radioratio').click(function () {
    $('.rollingsearchwordoptdiv').removeClass('hidden')
  })

  // Removes the second textbox when rolling ratio is not selected
  $('#radioaverage').click(function () {
    $('.rollingsearchwordoptdiv').addClass('hidden')
  })
})
