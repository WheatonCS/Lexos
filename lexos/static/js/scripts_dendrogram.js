import * as utility from './utility.js'

/**
 * the error message for the submission
 * @returns {string | null} - if it is null, it means no error, else then the string is the error message
 */
function submissionError () {
  const manageUrl = $('#manage-url').data().url
  const uploadUrl = $('#upload-url').data().url
  const activeFileNumTooFewErr = `You do not have enough active documents. 
  Please activate at least two documents using the <a href=${manageUrl}>Manage</a> tool 
  or <a href=${uploadUrl}>Upload</a> a new document.`
  const activeFiles = $('#num_active_files').val()
  if (activeFiles < 2) {
    return activeFileNumTooFewErr
  } else {
    return null
  }
}

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
 * When the HTML documents finish loading
 */
$(function () {
  /**
   * the events after dendrogram is clicked
   */
  $('#getdendro').on('click', function () {
    const error = submissionError() // the error happens during submission

    if (error === null) { // if there is no error
      generateDendrogram()
    } else {
      utility.runModal(error)
    }
  })
})
