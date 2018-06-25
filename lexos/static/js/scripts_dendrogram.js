import * as utility from './utility.js'

/**
 * the function to submit form via ajax in dendrogram
 * @returns {void} - nothing is returned from this function.
 */
function generateDendrogram () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/dendrogramDiv', form)
    .done(
      function (response) {
        $('#dendrogram-result').html(response)
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
 * Scrolls to dendrogram results after they are generated.
 */
function scrollToDendro () {
  $('html, body').animate({
    scrollTop: $('#dendrogram-result').offset().top
  }, 1000)
}

/**
 * When the HTML documents finish loading
 */
$(function () {
  /**
   * the events after dendrogram is clicked
   */
  $('#getdendro').on('click', function () {
    const error = utility.submissionError(2) // the error happens during submission

    if (error === null) { // if there is no error
      generateDendrogram()
      scrollToDendro()
    } else {
      utility.runModal(error)
    }
  })
})
