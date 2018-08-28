import * as utility from './utility.js'

/**
 * Show the milestone input when the milestone check box is checked.
 * @returns {void}.
 */
function updateMSopt () {
  if ($('#rollinghasmilestone').is(':checked')) {
    $('#rollingmilestoneopt').show()
  } else {
    $('#rollingmilestoneopt').hide()
  }
}

/**
 * Check possible errors existing in front end inputs.
 * @returns {string | null}: the errors that is checked by JS, if no error the result will be null.
 */
function getSubmissionError () {
  // Select the two input pattern.
  const searchPatternNumerator = $('#rollingsearchword')
  const searchPatternDenominator = $('#rollingsearchwordopt')
  // Get number of terms in both input pattern inputs.
  const numeratorLen = searchPatternNumerator.val().split(',').length
  const denominatorLen = searchPatternDenominator.val().split(',').length
  // Check if enough files were uploaded.
  const notEnoughFile = utility.submissionError(1)

  // Check all other possible errors.
  if (notEnoughFile !== null) {
    return notEnoughFile
  } else if ($('#rollingwindowsize').val() === '' || searchPatternNumerator.val() === '') {
    return `Please fill out both "Search Pattern(s)" and "Size of Rolling Window" fields.`
  } else if ($('#inputword').prop('checked') && $('#windowletter').prop('checked')) {
    return `You cannot use tokens for search terms when analyzing a window of characters. 
            The window setting has been changed to a window of tokens.`
  } else if ($('#rollingratio').prop('checked') && numeratorLen !== denominatorLen) {
    return `You have to put equal number of terms in both "Search Pattern(s)" numerator and 
            denominator. Separate terms by comma.`
  } else {
    return null
  }
}

/**
 * The function to submit form via ajax in dendrogram.
 * @returns {void}.
 */
function generateRollingWindow () {
  // show loading icon
  $('#status-visualize').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/rollingWindowGraph', form)
    .done(
      function (response) {
        $('#rwa-result-graph').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('Error encountered while plotting the rolling window analysis.')
      })
    .always(
      function () {
        $('#status-visualize').css({'visibility': 'hidden'})
      })
}

/* document.ready() Functions */
$(function () {
  // Get the rolling window result div.
  const resultDiv = $('#rwa-result')
  resultDiv.css({'visibility': 'hidden'})
  // Call update milestone on page load
  updateMSopt()
  // Bind the function to the checkbox
  $('#rollinghasmilestone').click(updateMSopt)

  $('#get-graph').click(function () {
    resultDiv.css({'visibility': 'hidden'})
    /* Get the possible validations. */
    const errorString = getSubmissionError()
    if (errorString === null) {
      generateRollingWindow()
      resultDiv.css({'visibility': 'visible'})
      utility.scrollToDiv(resultDiv)
    } else {
      utility.runModal(errorString)
    }
  })

  $('#download-csv').click(function (event) {
    /* Get the possible validations. */
    const errorString = getSubmissionError()
    if (errorString !== null) {
      event.preventDefault()
      utility.runModal(errorString)
    }
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
