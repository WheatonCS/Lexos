$(function () {
  if ($('input[name=\'haveGutenberg\']')) {
    $('#gutenberg-modal').modal()
  }
  $('#actions').addClass('actions-scrub')

  $('.has-chevron').click(function (ev) {
    rotateChevron(ev.currentTarget)
  })

  $('#save-button').on('click', function (e) {
    e.preventDefault()
    let tagDict = {}
    const serializedForm = $(this).closest('form').serializeArray()
    $.each(serializedForm, function () {
      // name and value
      if (tagDict[this.name] !== undefined) {
        if (!tagDict[this.name].push) {
          tagDict[this.name] = [tagDict[this.name]]
        }
        tagDict[this.name].push(this.value || '')
      } else {
        tagDict[this.name] = this.value || ''
      }
    })
    tagDict = JSON.stringify(tagDict)
    console.log(tagDict)
    $.ajax({
      type: 'POST',
      url: '/xml',
      data: tagDict,
      contentType: 'application/json;charset=UTF-8',
      cache: false,
      beforeSend: function () {
        $('#xml-modal-status').show()
      },
      success: function (response) {
        $('#xml-modal-status').hide()
        $('.modal.in').modal('hide')
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $('#error-modal .modal-body').html('Lexos could not perform the requested function.')
        $('#error-modal').modal()
        console.log('bad: ' + textStatus + ': ' + errorThrown)
      }
    })
  })

  // display additional options on load
  displayAdditionalOptions()

  /**
 * Clone file labels and do ajax request
 * @returns {void} - returns nothing
 */
  $('.bttnfilelabels').click(function () {
    // swfileselect, lemfileselect, consfileselect, scfileselect
    const filetype = $(this).attr('id').replace('bttnlabel', '')
    const usingCache = $('#usecache' + filetype).attr('disabled') !== 'disabled'

    if ((usingCache) || ($(this).attr('id') !== '')) {
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

  /**
 * Change white space box class when checked or unchecked
 * @returns {void} - returns nothing
 */
  $('#whitespacebox').click(function () {
    if ($(this).is(':checked')) {
      $('#whitespace').removeClass('hidden')
    } else {
      $('#whitespace').addClass('hidden')
    }
  })

  /**
 * Use special character options
 * @returns {void} - returns nothing
 */
  $('#entityrules').change(function () {
    console.log($('#entityrules').value)
    if ($('#entityrules')[0].value === 'MUFI-3' || $('#entityrules').value === 'MUFI-4') {
      document.getElementById('MUFI-warning').style.display = 'inline-block'
      $('head').append('<link href=\'../static/lib/junicode/Junicode.woff\' rel=\'stylesheet\' type=\'text/css\'>')
      $('.filecontents').addClass('Junicode')
    } else {
      $('.filecontents').removeClass('Junicode')
      document.getElementById('MUFI-warning').style.display = 'none'
    }
  })

  /**
 * Change tag box class when checked or unchecked
 * @param {object} tagBox - scrub tags checkbox DOM element
 * @returns {void} - returns nothing
 */
  $('#tagbox').click(function () {
    if ($(this).is(':checked')) {
      $('#tag').removeClass('hidden')
    } else {
      $('#tag').addClass('hidden')
    }
  })

  $('#set-tags-button').click(setTagsButtonAjax())

  $('#punctbox').change(function (ev) {
    showPunctOptions(ev)
  })

  $('#xml-modal').on('show.bs.modal', xmlModalAjax())

  $('#xml-modal').on('hidden.bs.modal', removeEmptyTagTable())
})

/**
 * Download the scrubbing results
 * @returns {void} - returns nothing
 */
function downloadScrubbing () { // eslint-disable-line no-unused-vars
  // Unfortunately, you can't trigger a download with an ajax request; calling a
  // Flask route seems to be the easiest method.
  window.location = '/downloadScrubbing'
}

/**
 * Send ajax request to do scrubbing
 * @param {string} action - preview or apply
 * @returns {void} - returns nothing
 */
function sendScrubbing (action) { // eslint-disable-line no-unused-vars
  if ($('#num_active_files').val() === '0') {
    const msg = 'You have no active documents. Please activate at least one document using the <a href="./manage">Manage</a> tool or <a href="./upload">upload</a> a new document.'
    $('#error-modal-message').html(msg)
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
      console.log(`bad: ${textStatus}: ${errorThrown}`)
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
 * @param {string} chevContainer - legend containing chevron
 * @returns {void} - returns nothing
 */
function rotateChevron (chevContainer) {
  $(chevContainer).find('span').toggleClass('down')
  $(chevContainer).next().collapse('toggle')
}

/**
 * Get additional options and truncate file names when necessary
 * @returns {void} - returns nothing
 */
function displayAdditionalOptions () {
  const advancedOptions = $('#advanced-title')
  advancedOptions.find('.icon-arrow-right').addClass('showing')
  advancedOptions.siblings('.expansion').slideToggle(0)

  $('#swfileselect').change(function (ev) {
    truncateFileName(ev, '#swfileselectbttnlabel')
  })

  $('#lemfileselect').change(function (ev) {
    truncateFileName(ev, '#lemfileselectbttnlabel')
  })

  $('#consfileselect').change(function (ev) {
    truncateFileName(ev, '#consfileselectbttnlabel')
  })

  $('#scfileselect').change(function (ev) {
    truncateFileName(ev, '#scfileselectbttnlabel')
  })
}

/**
 * Truncate file names if needed
 * @param {jQuery.Event} ev - jQuery event object
 * @param {string} container - id of file label container
 * @returns {void} - returns nothing
 */
function truncateFileName (ev, container) {
  let fileName = ev.target.files[0].name
  if (fileName.length > 25) { fileName = fileName.substring(0, 24) + '...' }
  $(container).html(fileName)
}

/**
 * Function to send ajax request for tags button
 * @returns {void} - returns nothing
 */
function setTagsButtonAjax () {
  if ($('#allTags')) {
    let allTags = ($('#allTags').value)
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
        console.log(`Error: ${errorThrown}`)
      }
    })
  }
}

/**
 * Display additional punctuation options when appropriate
 * @param {jQuery.Event} ev - change event to trigger function
 * @returns {void} - returns nothing
 */
function showPunctOptions (ev) {
  if($(ev.currentTarget).hasClass('checked')){
    $('#aposhyph').css({visibility: 'visible'})
  }
  else{
    $('#aposhyph').css({visibility: 'hidden'})
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
      $('#tagTable').append(`<thead><tr><th>Element</th><th>Action</th><th> ${select} </th></tr></thead>`)
      $('#tagTable').append('<tbody></tbody>')
      $('#tagTable tbody').append(j['menu'])
      $('#xmlModalStatus').remove()
      if (j['selected-options'] !== 'multiple') {
        $('#allTags option[value=\'' + j['selected-options'] + '\']').prop('selected', true)
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      console.log(`Error: ${errorThrown}`)
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
