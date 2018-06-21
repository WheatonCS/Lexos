import * as utility from './utility.js'

/**
 * Check if allow comparison among classes or classes to corpus.
 * @returns {void}
 */
function checkAllowClassComparison () {
  const enableClassComparison = $('#num-active-classes').data().number < 2
  $('#classToPara').attr('disabled', enableClassComparison)
  $('#classToClass').attr('disabled', enableClassComparison)
  /* Displays the class message if there is less than 2 classes assigned*/
  if (enableClassComparison) {
    $('#classInfo').show()
  } else {
    $('#classInfo').hide()
  }
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
 * Display the result of the top words on web page.
 * @returns {void}
 */
function generateTopWordResult () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/topwordResult', form)
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
        console.log(`textStatus: ${textStatus}`)
        console.log(`errorThrown: ${errorThrown}`)
        utility.runModal('Error encountered while generating the topword result.')
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
   * The event handler for generate top word clicked
   */
  $('#get-topwords').click(function () {
    const error = utility.submissionError(2) // The error happens during submission
    if (error === null) { // if there is no error
      generateTopWordResult()
    } else {
      utility.runModal(error)
    }
  })
})
