import * as utility from './utility.js'

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

/**
 * the function to submit form via ajax in dendrogram
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

/**
 * the function to submit form via ajax in dendrogram
 */
function displayMileStone () {
  // show loading icon
  $('#status-visualize').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/rollingWindowMileStone', form)
    .done(
      function (response) {
        if (response !== "") {
          const mile_stones = response.map(function (mile_stone) {
            return `<div class="col-sm-1 col-md-1 col-lg-1">
                        <p style="color: ${mile_stone['color']}; font-size: 20px">${mile_stone['mile_stone']}</p>
                    </div>`
          })
          $('#mile-stones').html(mile_stones)
          $('#mile-stone-field').css('display', 'block')
        }
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
  // Call update milestone on page load
  updateMSopt()
  // Bind the function to the checkbox
  $('#rollinghasmilestone').click(updateMSopt)

  $('#getgraph').click(function () {
    /* Validation */
    const errorString = getSubmissionError()
    if (errorString === null) {
      displayMileStone()
      generateRollingWindow()
    }

    else
      utility.runModal(errorString)
  })

  /* On-Click Validation */
  $('#radiowindowletter').click(function () {
    if ($('#inputword').prop('checked')) {
      $('#windowword').click()
      const msg = `You cannot use a window of characters when analyzing a token. 
                   The setting has been changed to a window of tokens.`
      utility.runModal(msg)
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
