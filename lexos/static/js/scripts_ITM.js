/* In the Margins Side Panel Functions */
/* Based on https://github.com/AndreaLombardo/BootSideMenu */
function getSide (listClasses) {
  var side
  for (var i = 0; i < listClasses.length; i++) {
    if (listClasses[i] == 'sidebar-left') {
      side = 'left'
      break
    } else if (listClasses[i] == 'sidebar-right') {
      side = 'right'
      break
    } else {
      side = null
    }
  }
  return side
}

function doAnimation (container, containerWidth, sidebarSide, sidebarStatus) {
  var toggler = container.children()[1]
  if (sidebarStatus == 'opened') {
    if (sidebarSide == 'left') {
      container.animate({
        left: -(containerWidth + 32)
      })
      toggleArrow('left')
    } else if (sidebarSide == 'right') {
      container.animate({
        right: -(containerWidth + 2)
      })
      toggleArrow('right')
    }
    container.attr('data-status', 'closed')
  } else {
    if (sidebarSide == 'left') {
      container.animate({
        left: 0
      })
      toggleArrow('right')
    } else if (sidebarSide == 'right') {
      container.animate({
        right: 0
      })
      toggleArrow('left')
    }
    container.attr('data-status', 'opened')
  }
}

function toggleArrow (side) {
  if (side == 'left') {
    $('#toggler').children('.glyphicon-chevron-right').css('display', 'block')
    $('#toggler').children('.glyphicon-chevron-left').css('display', 'none')
  } else if (side == 'right') {
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
      processData(data, type, url)
    },
    error: handleError
  })
}

function handleError (XMLHttpRequest, textStatus, errorThrown) {
  var error_msg = 'Lexos cannot load <em>In the Margins</em> content from Scalar. '
  error_msg += 'There may be a problem with your internet connection. If you think '
  error_msg += 'your internet connection is working, try accessing <em>In the '
  error_msg += "Margins</em> content directly from the <a href='https://scalar.usc.edu/works/lexos/' target='_blank'>"
  error_msg += 'Scalar website</a>.'
  $('#error-modal-message').html(error_msg)
  $('#error-modal').modal()
}

function processData (data, type, url) {
  for (var nodeProp in data) {
    node = data[nodeProp]
    content_path = node['http://rdfs.org/sioc/ns#content']
    if (node['http://purl.org/dc/terms/title'] != null) {
      var title = node['http://purl.org/dc/terms/title'][0].value
      var url = node['http://purl.org/dc/terms/isVersionOf'][0].value
    }
    if (node['http://simile.mit.edu/2003/10/ontologies/artstor#url'] != null) {
      var video_url = node['http://simile.mit.edu/2003/10/ontologies/artstor#url'][0].value
            // var url = node['http://purl.org/dc/terms/isVersionOf'][0].value;
    }
    if (node['http://simile.mit.edu/2003/10/ontologies/artstor#url'] != null) {
      var url = node['http://purl.org/dc/terms/isVersionOf'][0].value
    }
    if (content_path != null) {
      var content = content_path[0].value
      content = content.replace(new RegExp('\r?\n\r?\n', 'g'), '<br><br>') // Replace line breaks
    }
  }
  displayITMcontent(content, title, url, type, video_url)
}

function displayITMcontent (content, title, url, type, video_url) {
    // Replace Scalar internal links with urls to Scalar
  content = content.replace(/<a href=\"/g, '<a href="http://scalar.usc.edu/works/lexos/')
  content = content.replace(/http:\/\/http:\/\/scalar.usc.edu\/works\/lexos\//g, 'http://')
  content = content.replace(/<a href=\"http:\/\/scalar/g, '<a target="_blank" href="http://scalar')

    // In case there is no internet connection or user is in local mode
  var error_msg = 'Lexos cannot load <em>In the Margins</em> content from Scalar. '
  error_msg += 'There may be a problem with your internet connection. If you think '
  error_msg += 'your internet connection is working, try accessing <em>In the '
  error_msg += "Margins</em> content directly from the <a href='https://scalar.usc.edu/works/lexos/' target='_blank'>"
  error_msg += 'Scalar website</a>.'

    // Fork here based on type
  switch (type) {
    case 'panel':
      $('#panel-content').remove()
      titleLink = '<h4><a href="' + url + '" target="_blank">' + title + '</a></h4>'
      if (content.length > 0) {
        $('#itm-content').append('<div id="panel-content">' + titleLink + content + '<br/></div>')
      } else {
        $('#itm-content').append('<div id="panel-content"><h4>' + error_msg + '</h4></div>')
      }
        // Next two lines determine the panel height and change on window resize
        // var height = $("#panel-content").visibleHeight()+"px";
        // $("#panel-content").css("height", height);
      $('#panel-status').hide()
      break

    case 'dialog':
      titleLink = '<a href="' + url + '" target="_blank">' + title + '</a>'
      $('#ITM-modal .modal-title').html(titleLink)
      msg = '<h4>This is just a sample modal. Ultimately, it will open a settings dialog, but for now it can be used as a trigger to display <em>In the Margins</em> content. Click the <strong>Show Video</strong> button to see some sample video content.</h4>'
      $('#ITM-modal .modal-body').empty()
      $('#ITM-modal .modal-body').append(msg)
      if (url.length > 8) {
        $('#ITM-modal .modal-body').append(content)
      } else {
        $('#itm-content').append('<h4>' + error_msg + '</h4></div>')
      }
      $('#dialog-status').hide()
      break

        // Works only with YouTube videos
    case 'video-dialog':
      var youtube_url = video_url.replace('https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
      titleLink = '<a href="' + url + '" target="_blank">' + title + '</a>'
      $('#ITM-modal .modal-title').html(titleLink)
      msg = '<h4>This is just a sample modal. Ultimately, it will open a settings dialog, but for now it can be used as a trigger to display <em>In the Margins</em> content. Click the <strong>Show Video</strong> button to see some sample video content.</h4>'
      $('#ITM-modal .modal-body').empty()
      $('#ITM-modal .modal-body').html('')
      if (youtube_url.length > 8) {
        $('#ITM-modal .modal-body').append('<iframe style="min-height:500px;min-width:99%;" src="' + youtube_url + '"></iframe>')
      } else {
        $('#itm-content').append('<h4>' + error_msg + '</h4></div>')
      }
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
    var slug = (dataSlug == '') ? 'index' : dataSlug
    if (!status) {
      status = 'closed'
    }
    doAnimation(container, containerWidth, side, status)
    if (status == 'closed') {
      $('#panel-status').show()
      callAPI(slug, 'panel')
    }
  })

    /* Populate a Bootstrap modal */
  $('#ITM-modal').on('show.bs.modal', function (e) {
    var button = $(e.relatedTarget) // Button that triggered the modal
    var slug = button.data('slug') // Extract info from data-slug attribute
    var type = button.data('type') // Extract info from data-type attribute
    $('#dialog-status').show()
    callAPI(slug, type)
        // callAPI("best-practices", "dialog");
  })

    /* Empty a Bootstrap modal */
  $('#ITM-modal').on('hide.bs.modal', function () {
    $('#ITM-modal').removeData('bs.modal')
    icon = $('#dialog-status').parent().html()
    $('#ITM-modal .modal-body').html('')
    $('#ITM-modal .modal-body').html(icon)
    $('#dialog-status').hide()
    callAPI('best-practices', 'dialog')
  })

    /* Handle Show Video Button in Bootstrap Modal */
/*    $('#show-video').click(function() {
        callAPI("how-to-read-a-dendrogram", "video-dialog")
    }); */
})

/* Initialise Bootstrap Modal */
$('#ITM-modal').modal()
