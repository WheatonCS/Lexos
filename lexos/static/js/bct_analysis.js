import * as utility from './utility.js'

/**
 * the function to submit form via ajax in dendrogram
 * @returns {void} - nothing is returned from this function.
 */
function generateBCT () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/dendrogramDiv', form)
    .done(
      function (response) {
        $('#bct-result').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('error encountered while plotting the dendrogram.')
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
