$(function () {
  $('.has-chevron').on('click', rotateChevron)

  $('input[type=radio][name=tokenType]').click(updateTokenizeCheckbox)

  updateTokenizeCheckbox()

  $('input[type=radio][name=normalizeType]').click(updateNorm)

  updateNorm()

  $('input[type=checkbox][name=mfwcheckbox]').click(updateMFWinput)

  updateMFWinput()

  $('input[type=checkbox][name=cullcheckbox]').click(updatecullinput)

  updatecullinput()

  $(window).scroll(changeSubmitDivPosition())

  $(window).scroll() // Call a dummy scroll event after everything is loaded.
})

/**
 * Update tokenize checkbox for selecting documents
 * @returns {void}
 */
function updateTokenizeCheckbox () {
  if ($('#tokenByWords').is(':checked')) {
    $('#inWordsOnly').hide()
  } else {
    $('#inWordsOnly').show()
  }
}

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
function updateMFWinput () {
  // If most frequent words is checked
  if ($('#MFW').is(':checked')) {
    // Show top number of words input
    $('span[id=mfwnumber-input]').show()
    // If culling is checked
    if ($('#culling').is(':checked')) {
      // Change CSS to make room
      $('#temp-label-div').css('max-height', '221px')
      $('#modifylabels').css('max-height', '160px')
    } else {
      $('#temp-label-div').css('max-height', '191px')
      $('#modifylabels').css('max-height', '130px')
    }
  } else {
    if ($('#culling').is(':checked')) {
      $('#temp-label-div').css('max-height', '191px')
      $('#modifylabels').css('max-height', '130px')
    } else {
      $('#temp-label-div').css('max-height', '161px')
      $('#modifylabels').css('max-height', '100px')
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
function updatecullinput () {
  // If culling is checked
  if ($('#culling').is(':checked')) {
    // Show documents number input
    $('span[id=cullnumber-input]').show()
    // If most frequent words is checked
    if ($('#MFW').is(':checked')) {
      // Change CSS to make room
      $('#temp-label-div').css('max-height', '221px')
      $('#modifylabels').css('max-height', '160px')
    } else {
      $('#temp-label-div').css('max-height', '191px')
      $('#modifylabels').css('max-height', '130px')
    }
  } else {
    if ($('#MFW').is(':checked')) {
      $('#temp-label-div').css('max-height', '191px')
      $('#modifylabels').css('max-height', '130px')
    } else {
      $('#temp-label-div').css('max-height', '161px')
      $('#modifylabels').css('max-height', '100px')
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

/**
 * Change position of submit div while scrolling the window
 * @returns {void}
 */
function changeSubmitDivPosition () {
  let timer
  // Timer stuff
  if (timer) {
    clearTimeout(timer)
  }
  // Timer to throttle the scroll event so it doesn't happen too often
  timer = setTimeout(throttleScrollTimer(), 10)
}

/**
 * Throttle the scroll event so it doesn't happen too often
 * @returns {void}
 */
function throttleScrollTimer () {
  let buttonsFixed = false
  let buttons = $('#analyze-submit')
  let scrollBottom = $(window).scrollTop() + $(window).height()

  // if bottom of scroll window at the footer, allow buttons to rejoin page as it goes by
  if ((buttonsFixed && (scrollBottom >= ($('footer').offset().top)))) {
    // console.log("Scroll bottom hit footer! On the way down");
    buttons.removeClass('fixed')
    buttonsFixed = false
  }

  // if bottom of scroll window at the footer, fix button to the screen
  if (!buttonsFixed && (scrollBottom < ($('footer').offset().top))) {
    // console.log("Scroll bottom hit footer! On the way up");
    buttons.addClass('fixed')
    buttonsFixed = true
  }
}
