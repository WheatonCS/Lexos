$(function () {
  $('.has-chevron').on('click', function () {
    $(this).find('span').toggleClass('down')

    // Nasty hack because find("span") does not work in kmeans
    $(this).find('#kmeansAdvancedChev').toggleClass('down')
    $(this).find('#kmeansSilhouetteChev').toggleClass('down')

    $(this).next().collapse('toggle')
  })

  function updateTokenizeCheckbox () {
    if ($('#tokenByWords').is(':checked')) {
      $('#inWordsOnly').hide()
    } else {
      $('#inWordsOnly').show()
    }
  }

  $('input[type=radio][name=tokenType]').click(updateTokenizeCheckbox)

  updateTokenizeCheckbox()

  function updateNorm () {
    if ($('#normalizeTypeRaw').is(':checked') || $('#normalizeTypeFreq').is(':checked')) {
      $('#tfidfspan').hide()
    } else {
      $('#tfidfspan').show()
    }
  }

  $('input[type=radio][name=normalizeType]').click(updateNorm)

  updateNorm()

  function updateMFWinput () {
    if ($('#MFW').is(':checked')) {
      $('span[id=mfwnumber-input]').show()
      if ($('#culling').is(':checked')) {
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
      $('span[id=mfwnumber-input]').hide()
    }
  }

  $('input[type=checkbox][name=mfwcheckbox]').click(updateMFWinput)

  updateMFWinput()

  function updatecullinput () {
    if ($('#culling').is(':checked')) {
      $('span[id=cullnumber-input]').show()
      if ($('#MFW').is(':checked')) {
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
      $('span[id=cullnumber-input]').hide()
    }
  }

  $('input[type=checkbox][name=cullcheckbox]').click(updatecullinput)

  updatecullinput()

  // Change position of submit div while scrolling the window
  var timer
  var buttonsFixed = false
  var buttons = $('#analyze-submit')

  $(window).scroll(function () {
    // Timer stuff
    if (timer) {
      clearTimeout(timer)
    }
    // Timer to throttle the scroll event so it doesn't happen too often
    timer = setTimeout(function () {
      var scrollBottom = $(window).scrollTop() + $(window).height()
      var scrollTop = $(window).scrollTop()

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
    }, 10)
  })

  $(window).scroll() // Call a dummy scroll event after everything is loaded.
})
