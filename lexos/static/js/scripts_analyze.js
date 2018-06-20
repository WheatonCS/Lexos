/**
 * Show the options for weighted counts normalization if selected and hide
 * these options when another normalization technique is selected
 * @returns {void}
 */
function updateNorm () {
  if ($('#normalizeTypeRaw').is(':checked') || $('#normalizeTypeFreq').is(':checked')) {
    $('#tfidfspan').hide()
  } else {
    $('#tfidfspan').show()
  }
}

/**
 * Change CSS to make room for most frequent words number input when most
 * frequent words is checked
 * @returns {void}
 */
function updateMfwInput () {
  // If most frequent words is checked
  if ($('#MFW').is(':checked')) {
    // Show top number of words input
    $('span[id=mfwnumber-input]').show()
    // If culling is checked
    if ($('#culling').is(':checked')) {
      // Change CSS to make room
      $('#temp-label-div').css('max-height', '210px')
      $('#modifylabels').css('max-height', '150px')
    } else {
      $('#temp-label-div').css('max-height', '180px')
      $('#modifylabels').css('max-height', '120px')
    }
  } else {
    if ($('#culling').is(':checked')) {
      $('#temp-label-div').css('max-height', '180px')
      $('#modifylabels').css('max-height', '120px')
    } else {
      $('#temp-label-div').css('max-height', '150px')
      $('#modifylabels').css('max-height', '90px')
    }
    // Hide most frequent words input if MFW is not checked
    $('span[id=mfwnumber-input]').hide()
  }
}

/**
 * Change CSS to make room for must be in x documents number input when culling
 * is checked
 * @returns {void}
 */
function updateCullInput () {
  // If culling is checked
  if ($('#culling').is(':checked')) {
    // Show documents number input
    $('span[id=cullnumber-input]').show()
    // If most frequent words is checked
    if ($('#MFW').is(':checked')) {
      // Change CSS to make room
      $('#temp-label-div').css('max-height', '210px')
      $('#modifylabels').css('max-height', '150px')
    } else {
      $('#temp-label-div').css('max-height', '180px')
      $('#modifylabels').css('max-height', '120px')
    }
  } else {
    if ($('#MFW').is(':checked')) {
      $('#temp-label-div').css('max-height', '180px')
      $('#modifylabels').css('max-height', '120px')
    } else {
      $('#temp-label-div').css('max-height', '150px')
      $('#modifylabels').css('max-height', '90px')
    }
    // Hide culling input if culling is not checked
    $('span[id=cullnumber-input]').hide()
  }
}

/**
 * Toggle chevron class in order to handle chevron drop down button rotate
 * animation
 * @returns {void}
 */
function rotateChevron () {
  $(this).find('span').toggleClass('down')

  $(this).next().collapse('toggle')
}

$(function () {
  // Update div/span height when the page first finish loading.
  updateNorm()
  updateMfwInput()
  updateCullInput()

  // Clock function has to stay in document ready function.
  $('.has-chevron').click(rotateChevron)
  $('input[type=radio][name=normalizeType]').click(updateNorm)
  $('input[type=checkbox][name=mfwcheckbox]').click(updateMfwInput)
  $('input[type=checkbox][name=cullcheckbox]').click(updateCullInput)
})

