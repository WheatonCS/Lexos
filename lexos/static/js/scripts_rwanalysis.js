// Show the milestone input when the milestone checkbox is checked

function updateMSopt () {
  if ($('#rollinghasmilestone').is(':checked')) {
    $('#rollingmilestoneopt').show()
  } else {
    $('#rollingmilestoneopt').hide()
  }
}

function getSubmissionError () {
  if (numActiveDocs === 0)
    return 'Please select a document to analyze.'

  else if ($('#rollingwindowsize')[0].value === '' || $('#rollingsearchword')[0].value === '')
    return 'Please fill out the \'Search Pattern(s)\' and \'Size of Rolling Window\' fields.'

  else if ($('#inputword').prop('checked') && $('#windowletter').prop('checked'))
    return 'You cannot use tokens for search terms when analyzing a window of characters. ' +
            'The window setting has been changed to a window of tokens.'
  else
      return null
}

/* document.ready() Functions */
$(function () {

  // Call update milestone on page load
  updateMSopt()
  // Bind the function to the checkbox
  $('#rollinghasmilestone').click(updateMSopt)

  // Handle the return to top links
  $('.to-top').click(function () {
    $('html, body').animate({ scrollTop: 0 }, 800)
    return false
  })

  $('#getgraph').click(function (e) {
    /* Validation */

  })

  /* On-Click Validation */
  $('#radiowindowletter').click(function () {
    if ($('#inputword').prop('checked')) {
      $('#windowword').click()
      msg = 'You cannot use a window of characters when analyzing a token. '
      msg += 'The setting has been changed to a window of tokens.'
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

  // Transfers the value when the input field is checkd
  $('#radioinputletter').click(function () {
    var oldVal = $('.rollinginput').val()
    $('.rollinginput').val(oldVal)
  })

  // Keyboard navigation
  $('.rollinginput').keyup(function (evt) {
    var theEvent = evt || window.event
    var key = theEvent.keyCode || theEvent.which
    if (key !== 8) { // 8 is backspace
      if ($(this).val().length > 1 && $('#inputletter').prop('checked')) {
        $(this).val($(this).val().slice(0, 1))
      }
    }
  })

  // Keyboard navigation
  $('#rollingwindowsize').keypress(function (evt) {
    var theEvent = evt || window.event
    var key = theEvent.keyCode || theEvent.which
    if (key !== 8) { // 8 is backspace
      key = String.fromCharCode(key)
      var regex = /[0-9]|\./
      if (!regex.test(key)) {
        theEvent.returnValue = false
        if (theEvent.preventDefault) theEvent.preventDefault()
      }
    }
  })
})
