/**
 * Function to create popover help for new lexos users.
 * @returns {void}
 */
function sidebarPopover () {
  if (localStorage.getItem('visited') !== 'yes') {
    localStorage.setItem('visited', 'yes')
    $('#toggler').popover({
      'html': 'true',
      'title': '<i>In the Margins</i>',
      'content': 'View instructions for any screen in Lexos by clicking the <i>In the Margins</i> tab.<br></div> <div class="text-center"><button type="button" id="gotit" class="btn btn-primary" style="background-color: #0068AF; margin-top: 5px">Got it!</button></div>'
    }).popover('show').data('bs.popover').tip().css({
      'width': '170px',
      'text-align': 'center'
    })
    $('#gotit').click(function () {
      $('#toggler').popover('destroy')
    })
    $('#toggler').click(function () {
      $('#toggler').popover('destroy')
    })
  }
}

$.fn.center = function () {
  this.css('top', Math.max(0, ((($(window).height()) - $(this).outerHeight()) / 2) - 200) + 'px')
  this.css('left', Math.max(0, (($(window).width() - $(this).outerWidth()) / 2)) + 'px')
  return this
}

$('form').attr('method', 'post')

$(function () {
  scrollTop()
  $('#getviz').click(function (e) {
    if (numActiveDocs < 1) {
      const msg = `You have no active documents. Please activate at least one document using the <a href="./manage">Manage</a> tool or <a href="./upload">upload</a> a new document.`
      $('#error-modal-message').html(msg)
      $('#error-modal').modal()
      e.preventDefault()
      return false
    } else if ($('input[name=\'segmentlist\']:checked').length < 1) {
      const msg = `You have no active documents. Please activate at least one document using the <a href="./manage">Manage</a> tool or <a href="./upload">upload</a> a new document.`
      $('#error-modal-message').html(msg)
      $('#error-modal').modal()
      e.preventDefault()
      return false
    }
  })
  sidebarPopover()

  $('[data-toggle="tooltip"]').tooltip()
  $('[data-toggle=popover]').popover({
    trigger: 'manual',
    animate: false,
    html: true,
    placement: 'right',
    template:
       `<div class="popover" onmouseover="$(this).mouseleave(function() {$(this).hide();});">
            <div class="arrow"></div>
            <h3 class="popover-title"></h3>
            <div class="popover-content"><p></p></div>
        </div>`
  }).click(function (e) {
    e.preventDefault()
  }).mouseenter(function () {
    $(this).popover('show')
  })
  // Handle exceptions for submitting forms and display error messages on screen
  $('form').attr('method', 'post')
  $('form').submit(function () {
    $('#num_active_files').val()
    if ($('#num_active_files').val() === '0') {
      $('#error-modal').modal()
      return false
    } else {
      return true
    }
  })

  // Add "selected" class to parent of selected link
  $('.sublist li .selected').parents('.headernavitem').addClass('selected')

  // display/hide expandable divs here
  $('.has-expansion .icon-arrow-right').click(function () {
    $(this).toggleClass('showing')

    $(this).parent('legend').siblings('.expansion').slideToggle(500)
  })

  // Gray out all disabled inputs
  $.each($('input'), function () {
    if ($(this).prop('disabled')) {
      $(this).parent('label').addClass('disabled')
    }
  })

  // Redirect all clicks on "Upload Buttons" to their file upload input
  $('.upload-bttn').click(function () {
    $(this).siblings('input[type=file]').click()
  })

  // Show the nested submenu of clustering when mouse hover over the corresponding navbar, otherwise hide the nested menu
  $('#clustering-menu, #clustering-submenu').mouseover(function () {
    $('#clustering-submenu').css({'opacity': 1, 'visibility': 'visible'})
  }).mouseleave(function () {
    $('#clustering-submenu').css({'opacity': 0, 'visibility': 'hidden'})
  })

  // Highlight the nested label of the navBar when nested pages are active
  if ($('.nestedElement').hasClass('selected')) {
    $('.nestedLabel').addClass('selected')
  }

  $(document).on('click', '#savesettings', function (event) {
    event.preventDefault()
    let form = {}
    $.each($('#settingsform').serializeArray(), function (i, field) {
      form[field.name] = field.value || ''
    })

    if ($('#beta_onbox').is(':checked')) {
      form['beta_onbox'] = true
    } else {
      $.extend(form, {'beta_onbox': false})
    }
    $.ajax({
      'url': '/updatesettings',
      'type': 'POST',
      'contentType': 'application/json; charset=utf-8',
      'dataType': 'json',
      'data': JSON.stringify(form),
      'error': function () {
        alert('Error! Your settings could not be saved.')
      }
    }).done(function () {
      window.location = window.location.pathname
    })
  })
})

/**
 * Gathers all the form values and returns them as a FormData object. In Flask,
 * access for values through request.form and files through request.files.
 * Returns a JSON object.
 * @returns {json} response - response of the return call
 */
function getFormValues () {
  /* Gathers all the form values and returns them as a FormData object. In Flask,
  access form values through request.form and files through request.files. Returns
  a JSON object. */

  let formData = new FormData($('form')[0])

  $.ajax({
    url: '/previewScrubbing',
    type: 'POST',
    processData: false, // important
    contentType: false, // important
    data: formData,
    'error': function () { alert('error') }
  }).done(function (response) {
    response = JSON.parse(response)
    return response
  })
}

/***
 * Button that enables the window to go to the top of the page on a click.
 * @return {void}
 */
function scrollTop () {
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('#scroll').fadeIn()
    } else {
      $('#scroll').fadeOut()
    }
  })
  $('#scroll').click(function () {
    $('html, body').animate({ scrollTop: 0 }, 600)
    return false
  })
}
