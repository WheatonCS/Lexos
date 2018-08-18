import * as utility from './utility.js'

/**
 * The function to generate bootstrap consensus result.
 * @returns {void} - nothing is returned from this function.
 */
function generateBCT () {
  // Show loading icon.
  $('#status-analyze').css({'visibility': 'visible'})

  // Convert form into an object map string to string
  const form = utility.jsonifyForm()

  // Send the ajax request
  utility.sendAjaxRequest('/bct_analysis_result', form)
    .done(
      function (response) {
        $('#bct-result').html(`<img src="data:image/png;base64,${response}">`)
      })
    .fail(
      function () {
        utility.runModal('Error encountered while generating the bootstrap consensus result.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}

/**
 * When the HTML documents finish loading.
 */
$(function () {
  /**
   * The events after generate BCT is clicked.
   */
  $('#get-bct').on('click', function () {
    // Catch the possible error happens during submission.
    const error = utility.submissionError(2)

    if (error === null) { // If there is no error.
      generateBCT()
      utility.scrollToDiv($('#bct-result'))
    } else {
      utility.runModal(error)
    }
  })
})
