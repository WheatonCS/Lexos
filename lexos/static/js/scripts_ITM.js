/* In the Margins Side Panel Functions */
/* Based on https://github.com/AndreaLombardo/BootSideMenu */
function getSide (listClasses) {
  var side
  for (var i = 0; i < listClasses.length; i++) {
    if (listClasses[i] === 'sidebar-left') {
      side = 'left'
      break
    } else if (listClasses[i] === 'sidebar-right') {
      side = 'right'
      break
    } else {
      side = null
    }
  }
  return side
}

function doAnimation (container, containerWidth, sidebarSide, sidebarStatus) {
  // var toggler = container.children()[1]
  if (sidebarStatus === 'opened') {
    if (sidebarSide === 'left') {
      container.animate({
        left: -(containerWidth + 32)
      })
      toggleArrow('left')
    } else if (sidebarSide === 'right') {
      container.animate({
        right: -(containerWidth + 2)
      })
      toggleArrow('right')
    }
    container.attr('data-status', 'closed')
  } else {
    if (sidebarSide === 'left') {
      container.animate({
        left: 0
      })
      toggleArrow('right')
    } else if (sidebarSide === 'right') {
      container.animate({
        right: 0
      })
      toggleArrow('left')
    }
    container.attr('data-status', 'opened')
  }
}

function toggleArrow (side) {
  if (side === 'left') {
    $('#toggler').children('.glyphicon-chevron-right').css('display', 'block')
    $('#toggler').children('.glyphicon-chevron-left').css('display', 'none')
  } else if (side === 'right') {
    $('#toggler').children('.glyphicon-chevron-left').css('display', 'block')
    $('#toggler').children('.glyphicon-chevron-right').css('display', 'none')
  }
}

/* In the Margins API Functions */
function callAPI (slug, type) {
  // No reason not to hard code this here since we only need the slug
  var url = 'http://scalar.usc.edu/works/lexos/rdf/node/' + slug + '?rec=0&format=json'

  // Ajax call
  $.ajax({
    type: 'GET',
    url: url,
    dataType: 'jsonp',
    success: function (data) {
      console.log('Data received from server. Processing...')
      alert(JSON.stringify(data))
      processData(data, type, url)
    },
    error: handleError
  })
}

function handleError (XMLHttpRequest, textStatus, errorThrown) {
  var errorMsg = 'Lexos cannot load <em>In the Margins</em> content from Scalar. '
  errorMsg += 'There may be a problem with your internet connection. If you think '
  errorMsg += 'your internet connection is working, try accessing <em>In the '
  errorMsg += "Margins</em> content directly from the <a href='https://scalar.usc.edu/works/lexos/' target='_blank'>"
  errorMsg += 'Scalar website</a>.'
  $('#error-modal-message').html(errorMsg)
  $('#error-modal').modal()
}

function processData (data, type, url) {
  var title = '_'
  var content = '_'
  var videoUrl = '_'
  for (var nodeProp in data) {
    var node = data[nodeProp]
    console.log(JSON.stringify(node))
    var contentPath = node['http://rdfs.org/sioc/ns#content']
    if (node['http://purl.org/dc/terms/title'] != null) {
      title = node['http://purl.org/dc/terms/title'][0].value
      // url = node['http://purl.org/dc/terms/isVersionOf'][0].value
    }
    if (node['http://simile.mit.edu/2003/10/ontologies/artstor#url'] != null) {
      videoUrl = node['http://simile.mit.edu/2003/10/ontologies/artstor#url'][0].value
      // url = node['http://purl.org/dc/terms/isVersionOf'][0].value
    }
    if (node['http://simile.mit.edu/2003/10/ontologies/artstor#url'] != null) {
      // url = node['http://purl.org/dc/terms/isVersionOf'][0].value
    }
    if (contentPath != null) {
      content = contentPath[0].value
      content = content.replace(new RegExp('\r?\n\r?\n', 'g'), '<br><br>') // Replace line breaks
    } else {
      content = '_'
    }
    // Hack to make sure the loop stops once Lexos gets the information it needs
    if (title !== '_') {
      console.log('Displaying content with the following information:')
      console.log('content:' + content)
      console.log('title:' + title)
      console.log('url:' + url)
      console.log('type:' + type)
      console.log('videoURL:' + videoUrl)
      displayITMcontent(content, title, url, type, videoUrl)
    }
  }
}

function displayITMcontent (content, title, url, type, videoUrl) {
//   console.log('content:' + content)
//   console.log('title:' + title)
//   console.log('url:' + url)
//   console.log('type:' + type)
//   console.log('videoUrl:' + videoUrl)

  // Replace Scalar internal links with urls to Scalar
  content = content.replace(/<a href="/g, '<a href="http://scalar.usc.edu/works/lexos/')
  content = content.replace(/http:\/\/http:\/\/scalar.usc.edu\/works\/lexos\//g, 'http://')
  content = content.replace(/<a href="http:\/\/scalar/g, '<a target="_blank" href="http://scalar')

  // In case there is no internet connection or user is in local mode
  var errorMsg = 'Lexos cannot load <em>In the Margins</em> content from Scalar. '
  errorMsg += 'There may be a problem with your internet connection. If you think '
  errorMsg += 'your internet connection is working, try accessing <em>In the '
  errorMsg += "Margins</em> content directly from the <a href='https://scalar.usc.edu/works/lexos/' target='_blank'>"
  errorMsg += 'Scalar website</a>.'

  // Fork here based on type
  switch (type) {
    case 'panel':
      $('#panel-content').remove()
      var titleLink = '<h4><a href="' + url + '" target="_blank">' + title + '</a></h4>'
      if (content.length > 0) {
        $('#itm-content').append('<div id="panel-content">' + titleLink + content + '<br/></div>')
      } else {
        $('#itm-content').append('<div id="panel-content"><h4>' + errorMsg + '</h4></div>')
      }
      // Next two lines determine the panel height and change on window resize
      // var height = $("#panel-content").visibleHeight()+"px";
      // $("#panel-content").css("height", height);
      $('#panel-status').hide()
      break

    case 'dialog':
      console.log('Display type is a modal.')
      titleLink = '<a href="' + url + '" target="_blank">' + title + '</a>'
      $('#ITM-modal .modal-title').html(titleLink)
      var msg = '<h4>This is just a sample modal. Ultimately, it will open a settings dialog, but for now it can be used as a trigger to display <em>In the Margins</em> content. Click the <strong>Show Video</strong> button to see some sample video content.</h4>'
      $('#ITM-modal .modal-body').empty()
      $('#ITM-modal .modal-body').append(msg)
      if (url.length > 8) {
        $('#ITM-modal .modal-body').append(content)
      } else {
        $('#itm-content').append('<h4>' + errorMsg + '</h4></div>')
      }
      console.log('Bad modal launch.')
      $('#ITM-modal').modal()
      $('#dialog-status').hide()
      break

    // Works only with YouTube videos
    case 'video-dialog':
      $('#dialog-status').show()
      console.log('Display type is a video modal.')
      var youtubeUrl = videoUrl.replace('https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
      titleLink = '<a href="' + url + '" target="_blank">' + title + '</a>'
      $('#ITM-modal .modal-title').html(titleLink)
      msg = '<h4>This is just a sample modal. Ultimately, it will open a settings dialog, but for now it can be used as a trigger to display <em>In the Margins</em> content. Click the <strong>Show Video</strong> button to see some sample video content.</h4>'
      $('#ITM-modal .modal-body').empty()
      $('#ITM-modal .modal-body').html('')
      if (youtubeUrl.length > 8) {
        $('#ITM-modal .modal-body').append('<iframe style="min-height:500px;min-width:99%;" src="' + youtubeUrl + '"></iframe>')
      } else {
        $('#itm-content').append('<h4>' + errorMsg + '</h4></div>')
      }
      console.log('Launch video modal.')
      $('#ITM-modal').modal()
      $('#dialog-status').hide()
      break
  }
}

/* Gets the height of the viewport relative to a specified element.
   See http://stackoverflow.com/questions/24768795/get-the-visible-height-of-a-div-with-jquery */
$.fn.visibleHeight = function () {
  var elBottom, elTop, scrollBot, scrollTop, visibleBottom, visibleTop
  scrollTop = $(window).scrollTop()
  scrollBot = scrollTop + $(window).height()
  elTop = this.offset().top
  elBottom = elTop + this.outerHeight()
  visibleTop = elTop < scrollTop ? scrollTop : elTop
  visibleBottom = elBottom > scrollBot ? scrollBot : elBottom
  return visibleBottom - visibleTop
}

/* Document Ready Functions */
$(document).ready(function () {
  /* Get the viewport height after the window is resized */
  // $(window).on('scroll resize', getVisible);

  /* ITM Panel Setup */
  var container = $('#toggler').parent()
  var containerWidth = container.width()
  container.css({left: -(containerWidth + 32)})
  container.attr('data-status', 'closed')

  /* ITM Panel Toggle Events */
  /* Note: This function currently only works with side-panel toggle icon.
       To enable the use of other triggers, a class trigger should be used. */
  $('#cog-toggler').click(function (e) {
    e.preventDefault()
    $('#settings-modal').modal('hide')
    $('#toggler').click()
  })
  $('#toggler').click(function () {
    var container = $(this).parent()
    var listClasses = $(container[0]).attr('class').split(/\s+/) // IE9 Fix
    var side = getSide(listClasses)
    var containerWidth = container.width()
    var status = container.attr('data-status')
    var dataSlug = $('#ITMPanel-itm-content').attr('data-slug')
    var slug = (dataSlug === '') ? 'index' : dataSlug
    if (!status) {
      status = 'closed'
    }
    doAnimation(container, containerWidth, side, status)
    if (status === 'closed') {
      $('#panel-status').show()
      console.log('Calling API from ITM panel')
      callAPI(slug, 'panel')
    }
  })

  /* Populate a Bootstrap modal */
//   $('#ITM-modal').on('show.bs.modal', function (e) {
//     var button = $(e.relatedTarget) // Button that triggered the modal
//     var slug = button.data('slug') // Extract info from data-slug attribute
//     var type = button.data('type') // Extract info from data-type attribute
//     $('#dialog-status').show()
//     console.log('Calling API after opening Bootstrap modal.')
//     callAPI(slug, type)
//     // callAPI("best-practices", "dialog");
//   })
  $('.bttn-video').on('click', function (e) {
    var slug = $(this).children().first().data('slug') // Extract info from data-slug attribute
    var type = $(this).children().first().data('type') // Extract info from data-type attribute
    $('#dialog-status').show()
    console.log('Calling API after click with slug "' + slug + '" and type "' + type + '".')
    callAPI(slug, type)
  })

  /* Empty a Bootstrap modal */
  $('#ITM-modal').on('hide.bs.modal', function () {
    $('#ITM-modal').removeData('bs.modal')
    var icon = $('#dialog-status').parent().html()
    $('#ITM-modal .modal-body').html('')
    $('#ITM-modal .modal-body').html(icon)
    $('#dialog-status').hide()
    console.log('Hiding Bootsrap modal.')
    // callAPI('best-practices', 'dialog')
  })

  /* Handle Show Video Button in Bootstrap Modal */
//   $('.bttn-video').click(function (e) {
//     e.preventDefault()
//     var slug = $(this).children().first().attr('data-slug')
//     // callAPI(slug, 'video-dialog')
//   })
})

/* Initialise Bootstrap Modal */
$('#ITM-modal').modal()
