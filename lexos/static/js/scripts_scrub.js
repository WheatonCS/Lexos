$(function () {
  if ($('input[name=\'haveGutenberg\']')) {
    $('#gutenberg-modal').modal()
  }
  $('#actions').addClass('actions-scrub')

  $('.has-chevron').click(rotateChevron())

  // display additional options on load
  const advancedOptions = $('#advanced-title')
  advancedOptions.find('.icon-arrow-right').addClass('showing')
  advancedOptions.siblings('.expansion').slideToggle(0)

  $('#swfileselect').change(function (ev) {
    let filename = ev.target.files[0].name
    if (filename.length > 25) { filename = filename.substring(0, 24) + '...' }
    $('#swfileselectbttnlabel').html(filename)
  })

  $('#lemfileselect').change(function (ev) {
    let filename = ev.target.files[0].name
    if (filename.length > 25) { filename = filename.substring(0, 24) + '...' }
    $('#lemfileselectbttnlabel').html(filename)
  })

  $('#consfileselect').change(function (ev) {
    let filename = ev.target.files[0].name
    if (filename.length > 25) { filename = filename.substring(0, 24) + '...' }
    $('#consfileselectbttnlabel').html(filename)
  })

  $('#scfileselect').change(function (ev) {
    let filename = ev.target.files[0].name
    if (filename.length > 25) { filename = filename.substring(0, 24) + '...' }
    $('#scfileselectbttnlabel').html(filename)
  })

  $('.bttnfilelabels').click(function () {
    // swfileselect, lemfileselect, consfileselect, scfileselect
    const filetype = $(this).attr('id').replace('bttnlabel', '')
    const usingCache = $('#usecache' + filetype).attr('disabled') != 'disabled'

    if ((usingCache) || ($(this).attr('id') != '')) {
      // $(this).siblings('.scrub-upload').attr('value', '');
      // Next two lines clear the file input; it's hard to find a cross-browser solution
      $('#' + filetype).val('')
      $('#' + filetype).replaceWith($('#' + filetype).clone(true))
      $('#usecache' + filetype).attr('disabled', 'disabled')
      $(this).text('')
    }

    // Do Ajax
    $.ajax({
      type: 'POST',
      url: '/removeUploadLabels',
      data: $(this).text().toString(),
      contentType: 'text/plain',
      headers: {'option': filetype + '[]'},
      beforeSend: function () {
        // alert('Sending...');
      },
      success: function (response) {
        // console.log(response);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log('Error: ' + errorThrown)
      }
    })
  })

  $('#whitespacebox').click(function () {
    if ($(this).is(':checked')) {
      $('#whitespace').removeClass('hidden')
    } else {
      $('#whitespace').addClass('hidden')
    }
  })
  $('#entityrules').change(function () {
    console.log($('#entityrules')[0].value)
    if ($('#entityrules')[0].value == 'MUFI-3' || $('#entityrules')[0].value == 'MUFI-4') {
      document.getElementById('MUFI-warning').style.display = 'inline-block'
      $('head').append('<link href=\'../static/lib/junicode/Junicode.woff\' rel=\'stylesheet\' type=\'text/css\'>')
      $('.filecontents').addClass('Junicode')
    } else {
      $('.filecontents').removeClass('Junicode')
      document.getElementById('MUFI-warning').style.display = 'none'
    }
  })

  $('#tagbox').click(function () {
    if ($(this).is(':checked')) {
      $('#tag').removeClass('hidden')
    } else {
      $('#tag').addClass('hidden')
    }
  })

  $(document).on('click', '#set-tags-button', function (event) {
    if ($('#allTags')) {
      let allTags = ($('#allTags')[0].value)
      allTags = JSON.stringify(allTags)
      $.ajax({
        type: 'POST',
        url: '/setAllTagsTable',
        data: allTags,
        'contentType': 'application/json; charset=utf-8',
        'dataType': 'json',
        beforeSend: function () {
          $('<p/>', {
            id: 'xmlModalStatus',
            style: 'width:100px;margin:50px auto;z-index:1000;'
          }).appendTo('#xmlModalBody')
          $('#xmlModalStatus').append('<img src="/static/images/loading_icon.svg?ver=2.5" alt="Loading..."/>')
        },
        success: function (response) {
          const selection = $('#allTags option:selected').val()
          $('#tagTable').empty().remove()
          const t = '<table id="tagTable" class="table table-condensed table-striped table-bordered"></table>'
          $('#xmlModalBody').append(t)
          let select = '<select id="allTags" style="margin-top:3px;margin-right:5px;">'
          select += '<option value="remove-tag,allTags">Remove Tag Only</option>'
          select += '<option value="remove-element,allTags">Remove Element and All Its Contents</option>'
          select += '<option value="replace-element,allTags">Replace Element and Its Contents with Attribute Value</option>'
          select += '<option value="leave-alone,allTags">Leave Tag Alone</option>'
          select += '</select>'
          select += '<button id="set-tags-button" type="button" class="btn btn-primary"">Set All</button>'
          $('#tagTable').append('<thead><tr><th>Element</th><th>Action</th><th>' + select + '</th></tr></thead>')
          $('#tagTable').append('<tbody></tbody>')
          $('#tagTable tbody').append(response)
          $('#xmlModalStatus').remove()
          $('#allTags option[value=\'' + selection + '\']').prop('selected', true)
        },
        error: function (jqXHR, textStatus, errorThrown) {
          console.log('Error: ' + errorThrown)
        }
      })
    }
  })

  $('#punctbox').mousedown(function () {
    const timeToToggle = 300

    if ($('#aposhyph')[0].style.cssText == 'display: none;') {
      $('#aposhyph').fadeIn(timeToToggle)
    } else {
      $('#aposhyph').fadeOut(timeToToggle)
      $('#aposhyph')[0].style.cssText == 'display: none;'
    }
  })

  $('#xml-modal').on('show.bs.modal', function (e) {
    $.ajax({
      type: 'POST',
      url: '/getTagsTable',
      contentType: 'json',
      beforeSend: function () {
        $('<p/>', {
          id: 'xmlModalStatus',
          style: 'width:100px;margin:50px auto;z-index:1000;'
        }).appendTo('#xmlModalBody')

        $('#xmlModalStatus').append('<img src="/static/images/loading_icon.svg?ver=2.5" alt="Loading..."/>')
      },
      success: function (response) {
        j = JSON.parse(response)
        const t = '<table id="tagTable" class="table table-condensed table-striped table-bordered"></table>'
        $('#xmlModalBody').append(t)
        let select = '<select id="allTags" style="margin-top:3px;margin-right:5px;">'
        select += '<option value="remove-tag,allTags">Remove Tag Only</option>'
        select += '<option value="remove-element,allTags">Remove Element and All Its Contents</option>'
        select += '<option value="replace-element,allTags">Replace Element and Its Contents with Attribute Value</option>'
        select += '<option value="leave-alone,allTags">Leave Tag Alone</option>'
        select += '</select>'
        select += '<button id="set-tags-button" type="button" class="btn btn-primary"">Set All</button>'
        $('#tagTable').append('<thead><tr><th>Element</th><th>Action</th><th>' + select + '</th></tr></thead>')
        $('#tagTable').append('<tbody></tbody>')
        $('#tagTable tbody').append(j['menu'])
        $('#xmlModalStatus').remove()
        if (j['selected-options'] != 'multiple') {
          $('#allTags option[value=\'' + j['selected-options'] + '\']').prop('selected', true)
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log('Error: ' + errorThrown)
      }
    })
  })

  $('#xml-modal').on('hidden.bs.modal', function () {
    $('#tagTable').empty().remove()
  })
})

function downloadScrubbing () {
  // Unfortunately, you can't trigger a download with an ajax request; calling a
  // Flask route seems to be the easiest method.
  window.location = '/downloadScrubbing'
}

function doScrubbing (action) {
  if ($('#num_active_files').val() == '0') {
    $('#error-modal').modal()
    return
  }

  $('#status-prepare').css({'visibility': 'visible'})

  $('#formAction').val(action)
  const formData = new FormData($('form')[0])

  $.ajax({
    url: '/doScrubbing',
    type: 'POST',
    processData: false, // important
    contentType: false, // important
    data: formData,
    error: function (jqXHR, textStatus, errorThrown) {
      $('#error-modal-message').html('Lexos could not apply the scrubbing actions.')
      $('#error-modal').modal()
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    }
  }).done(function (response) {
    response = JSON.parse(response)
    $('#preview-body').empty()
    $.each(response['data'], function (i, item) {
      // const fileID = $(this)[0]
      const filename = $(this)[1]
      // const fileLabel = $(this)[2]
      const fileContents = $(this)[3]
      const fieldset = $('<fieldset></fieldset>')
      // CSS truncates the document name
      fieldset.append('<legend class="has-tooltip" style="color:#999; width:90%;margin: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + filename + '</legend>')
      fieldset.append('<div class="filecontents">' + fileContents + '</div>') // Keep this with no whitespace!
      $('#preview-body').append(fieldset)
      $('#status-prepare').css({'visibility': 'hidden'})
    })
  })
}

function rotateChevron () {
  $(this).find('span').toggleClass('down')
  $(this).next().collapse('toggle')
}
