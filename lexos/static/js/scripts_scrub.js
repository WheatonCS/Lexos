$(function () {
  if ($('input[name=\'haveGutenberg\']')) {
    $('#gutenberg-modal').modal()
  }
  $('#actions').addClass('actions-scrub')

  $('.has-chevron').click(function () {
    $(this).find('span').toggleClass('down')
    $(this).next().collapse('toggle')
  })

  // display additional options on load
  displayAdditionalOptions()

  $('.bttnfilelabels').click(buttonFileLabelsFunction())

  $('#whitespacebox').click(changeWhitespaceBoxClass()
  )
  $('#entityrules').change(entityRulesChangeFunction())

  $('#tagbox').click(changeTagBoxClass())

  $('#set-tags-button').click(setTagsButtonAjax())

  $('#punctbox').mousedown(puncTBoxFade())

  $('#xml-modal').on('show.bs.modal', xmlModalAjax())

  $('#xml-modal').on('hidden.bs.modal', removeEmptyTagTable())
})

/**
 * Download the scrubbing results
 * @returns {void} - returns nothing
 */
function downloadScrubbing () {
  // Unfortunately, you can't trigger a download with an ajax request; calling a
  // Flask route seems to be the easiest method.
  window.location = '/downloadScrubbing'
}

/**
 * Send ajax request to do scrubbing
 * @param {string} action - preview or apply
 * @returns {void} - returns nothing
 */
function sendScrubbing (action) {
  if ($('#num_active_files').val() === '0') {
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
    $.each(response['data'], function () {
      const fileName = $(this)[1]
      const fileContents = $(this)[3]
      // CSS truncates the document name
      const fieldSet = `<fieldset><legend class="has-tooltip"
      style="color:#999; width:90%;margin: auto; white-space: nowrap;
      overflow: hidden; text-overflow: ellipsis;">${fileName}</legend>
      <div class="filecontents">${fileContents}</div></fieldset> ` // Keep this with no whitespace!
      $('#preview-body').append(fieldSet)
      $('#status-prepare').css({'visibility': 'hidden'})
    })
  })
}

/**
 * Function to handle the chevron drop down button rotate animation by toggling
 * the class so the appropriate CSS applies.
 * @returns {void} - returns nothing
 */
function rotateChevron () {
  $(this).find('span').toggleClass('down')
  $(this).next().collapse('toggle')
}

/**
 * Get additional options and truncate file names when necessary
 * @returns {void} - returns nothing
 */
function displayAdditionalOptions () {
  const advancedOptions = $('#advanced-title')
  advancedOptions.find('.icon-arrow-right').addClass('showing')
  advancedOptions.siblings('.expansion').slideToggle(0)

  $('#swfileselect').change(truncateFileName())

  $('#lemfileselect').change(truncateFileName())

  $('#consfileselect').change(truncateFileName())

  $('#scfileselect').change(truncateFileName())
}

/**
 * Truncate file names if needed
 * @param ev - event? not sure how to pass in function call...
 * @returns {void}
 */
function truncateFileName (ev) {
  let fileName = ev.target.files[0].name
  if (fileName.length > 25) { fileName = fileName.substring(0, 24) + '...' }
  $(this).html(fileName)
}

/**
 * Clone file labels and do ajax request
 * @returns {void} - returns nothing
 */
function buttonFileLabelsFunction () {
  // swfileselect, lemfileselect, consfileselect, scfileselect
  const fileType = $(this).attr('id').replace('bttnlabel', '')
  const usingCache = $(`#usecache${fileType}`).attr('disabled') !== 'disabled'

  if ((usingCache) || ($(this).attr('id') !== '')) {
    // $(this).siblings('.scrub-upload').attr('value', '');
    // Next two lines clear the file input; it's hard to find a cross-browser solution
    $(`#${fileType}`).val('')
    $('#' + fileType).replaceWith($(`#${fileType}`).clone(true))
    $(`#${fileType}`).attr('disabled', 'disabled')
    $(this).text('')
  }
}

/**
 * Change white space box class when checked or unchecked
 * @returns {void} - returns nothing
 */
function changeWhitespaceBoxClass () {
  if ($(this).is(':checked')) {
    $('#whitespace').removeClass('hidden')
  } else {
    $('#whitespace').addClass('hidden')
  }
}

/**
 * Change tag box class when checked or unchecked
 * @returns {void} - returns nothing
 */
function changeTagBoxClass () {
  if ($(this).is(':checked')) {
    $('#tag').removeClass('hidden')
  } else {
    $('#tag').addClass('hidden')
  }
}

/**
 * Use special character options
 * @returns {void} - returns nothing
 */
function entityRulesChangeFunction () {
  console.log($('#entityrules')[0].value)
  if ($('#entityrules')[0].value === 'MUFI-3' || $('#entityrules')[0].value === 'MUFI-4') {
    $('#MUFI-warning').style.display = 'inline-block'
    $('head').append('<link href=\'../static/lib/junicode/Junicode.woff\' rel=\'stylesheet\' type=\'text/css\'>')
    $('.filecontents').addClass('Junicode')
  } else {
    $('.filecontents').removeClass('Junicode')
    $('#MUFI-warning').style.display = 'none'
  }
}

/**
 * Function to send ajax request for tags button
 * @returns {void} - returns nothing
 */
function setTagsButtonAjax () {
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
        const select = `<select id="allTags" style="margin-top:3px;margin-right:5px;">
        <option value="remove-tag,allTags">Remove Tag Only</option>
        <option value="remove-element,allTags">Remove Element and All Its Contents</option>
        <option value="replace-element,allTags">Replace Element and Its Contents with Attribute Value</option>
        <option value="leave-alone,allTags">Leave Tag Alone</option>
        </select>
        <button id="set-tags-button" type="button" class="btn btn-primary"">Set All</button>`
        $('#tagTable').append(`<thead><tr><th>Element</th><th>Action</th><th>${select}</th></tr></thead>`)
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
}

/**
 * Fade in/out animation
 * @returns {void} - returns nothing
 */
function puncTBoxFade () {
  const timeToToggle = 300

  if ($('#aposhyph')[0].style.cssText === 'display: none;') {
    $('#aposhyph').fadeIn(timeToToggle)
  } else {
    $('#aposhyph').fadeOut(timeToToggle)
  }
}

/**
 * Get document tags table
 * @returns {void} - returns nothing
 */
function xmlModalAjax () {
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
      const j = JSON.parse(response)
      const t = '<table id="tagTable" class="table table-condensed table-striped table-bordered"></table>'
      $('#xmlModalBody').append(t)
      const select = `<select id="allTags" style="margin-top:3px;margin-right:5px;">
      <option value="remove-tag,allTags">Remove Tag Only</option>
      <option value="remove-element,allTags">Remove Element and All Its Contents</option>
      <option value="replace-element,allTags">Replace Element and Its Contents with Attribute Value</option>
      <option value="leave-alone,allTags">Leave Tag Alone</option>
      </select>
      <button id="set-tags-button" type="button" class="btn btn-primary"">Set All</button>`
      $('#tagTable').append('<thead><tr><th>Element</th><th>Action</th><th>' + select + '</th></tr></thead>')
      $('#tagTable').append('<tbody></tbody>')
      $('#tagTable tbody').append(j['menu'])
      $('#xmlModalStatus').remove()
      if (j['selected-options'] !== 'multiple') {
        $('#allTags option[value=\'' + j['selected-options'] + '\']').prop('selected', true)
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log('Error: ' + errorThrown)
    }
  })
}

/**
 * Remove empty portions of tag table
 * @returns {void} - returns nothing
 */
function removeEmptyTagTable () {
  $('#tagTable').empty().remove()
}
