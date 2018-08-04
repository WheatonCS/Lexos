import * as utility from './utility.js'

/**
 * the function to submit form via ajax in dendrogram
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
      function () {
        $('#bct-result').html(`<img src="../../../test.png">`)
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
 * When the HTML documents finish loading
 */
$(function () {
  /**
   * the events after dendrogram is clicked
   */
  $('#get-bct').on('click', function () {
    // Catch the possible error happens during submission.
    const error = utility.submissionError(2)

    if (error === null) { // If there is no error
      generateBCT()
      utility.scrollToDiv($('#bct-result'))
    } else {
      utility.runModal(error)
    }
  })
})
