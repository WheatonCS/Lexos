/**
 * function to check if there are errors.
 */
function checkForErrors () {
  // Set Error and Warning Messages

  const errorMsg = doCheck()

  if (errorMsg !== '') {
    $('#hasErrors').val('true')
    $('#status-prepare').css({'visibility': 'hidden'})
    $('#error-modal-message').html(errorMsg)
    $('#error-modal').modal()
  }
  else {
    $('#hasErrors').val('false')
  }
}

/**
 * function to figure out where general errors are.
 * @returns {*}
 */
function doCheck () {
  const noActiveDocsMsg = `You have no active documents. Please \
  activate at least one document using the 
  <a href=\"{{ url_for("manage.manage") }}\">Manage</a> tool or 
  <a href=\"{{ url_for("upload.upload") }}\">upload</a> a new document.`
  const noCutStringMsg = 'You must provide a string to cut on.'
  const noCutValMsg = 'You must provide a default cutting value.'

  // Confirm that there are active files
  if ($('#numActiveFiles').val() === '0') {
    return noActiveDocsMsg
  }

  // If cut by milestone is checked make sure there is a milestone value
  if ($('#cutByMS').is(':checked')) {
    if ($('#MScutWord').val() === '') {
      return noCutStringMsg
    }
  }
  else {
    // Make sure there is a default cutting value
    if ($('#overallcutvalue').val() === '') {
      return noCutValMsg
    }
    else {
      return checkValues()
    }
  }
}

/**
 * function to figure out if errors with cut and overlap values.
 * @returns {string} - the error message.
 */
function checkValues () {
  const defInvalidSegSize = 'Default cutting: Invalid segment size.'
  const defInvalidOverlapVal = 'Default cutting: Invalid overlap value.'
  const indInvalidSegSize = 'Individual cutting: Invalid segment size.'
  const indInvalidOverlapVal = 'Individual cutting: Invalid overlap value.'

  const overallcutvalueStr = $('#overallcutvalue').val()
  const overallcutvalue = parseInt($('#overallcutvalue').val())
  const overallOverlapValue = parseInt($('#overallOverlapValue').val())
  const individualOverlap = parseInt($('#individualOverlap').val())
  const individualCutValueStr = $('#individualCutValue').val()
  let individualCutValue = $('#individualCutValue').val()

  // Make sure the overall segment size not negative
  if (overallcutvalue !== Math.floor(overallcutvalue)) {
    return defInvalidSegSize
  }
  // Make sure the overall segment size not a decimal
  if (overallcutvalueStr !== Math.abs(overallcutvalue).toString()) {
    return defInvalidSegSize
  }
  // Make sure the overall segment size not 0
  if (overallcutvalue === 0) {
    return defInvalidSegSize
  }
  // Make sure the overall overlap is valid
  if ((overallcutvalue <= overallOverlapValue) || (Math.abs(Math.round(overallOverlapValue)) !== overallOverlapValue)) {
    return defInvalidOverlapVal
  }
  // If there are individual segment cuts
  if (individualCutValue !== '') {
    individualCutValue = parseInt(individualCutValue)
    // Make sure the individual segment size not negative
    if (individualCutValue !== Math.floor(individualCutValue)) {
      return indInvalidSegSize
    }
    // Make sure the individual segment size not a decimal
    if (individualCutValueStr !== Math.abs(individualCutValue).toString()) {
      return indInvalidSegSize
    }
    // Make sure the individual segment size not 0
    if (individualCutValue === 0) {
      return indInvalidSegSize
    }
    // Make sure the individual overlap is valid
    if ((individualCutValue <= individualOverlap) || (Math.abs(Math.round(individualOverlap)) !== individualOverlap)) {
      return indInvalidOverlapVal
    }
  }
  return ''
}


/**
 * function to check whether the user needs a warning.
 */
function checkForWarnings () {
  let needsWarning = false
  const maxSegs = 100
  const defCutTypeValue = $("input[name='cutType']:checked").val() // Cut Type
  const cutVal = parseInt($("input[name='cutValue']").val()) // Segment Size
  const overVal = parseInt($('#overallOverlapValue').val()) // Overlap Size
  const indivDivs = $('.cuttingoptionswrapper.ind') // All individual cutsets
  const eltsWithoutIndividualOpts = [] // Elements without individual cutsets

  // Check each individual cutset
  indivDivs.each(function () {
    let thisCutVal = $('#individualCutValue', this).val() // Individual segment size
    let thisOverVal = $('#individualOverlap', this).val() // Individual overlap size
    // Parse as integers
    if (thisCutVal !== '') {
      thisCutVal = parseInt(thisCutVal)
      thisOverVal = parseInt(thisOverVal)
    }
    // Get a list of each of the cutset indices
    const listindex = indivDivs.index(this)
    const currID = activeFileIDs[listindex] // activeFileIDs is defined in the template file
    const isCutByMS = $('.indivMS', this).is(':checked') // True if cut by milestone checked
    // If not cut by milestone and no segment size, add to no individual cutsets array
    if (!isCutByMS && thisCutVal === '') {
      eltsWithoutIndividualOpts.push(listindex)
    }
    // If no segment size
    if (thisCutVal !== '') {
      // Get segment cut type
      const thisCutType = $(`input[name='cutType_${currID}']:checked`).val()
      // If not cut by milestone, use num_ variables set in template file
      if (!(isCutByMS)) {
        // Needs warning...
        // If the number of characters-overlap size/segment size-overlap size > 100
        if (thisCutType === 'letters' && (numChar[listindex] - thisOverVal) / (thisCutVal - thisOverVal) > maxSegs) {
          needsWarning = true
          // Same for segments and lines
        }
        else if (thisCutType === 'words' && (numWord[listindex] - thisOverVal) / (thisCutVal - thisOverVal) > maxSegs) {
          needsWarning = true
        }
        else if (thisCutType === 'lines' && (numLine[listindex] - thisOverVal) / (thisCutVal - thisOverVal) > maxSegs) {
          needsWarning = true
          // Or if the segment size > 100
        }
        else if (thisCutVal > maxSegs && eltsWithoutIndividualOpts.length > 0) {
          needsWarning = true
        }
      }
    }
  })

  // If cut by milestone is checked
  if ($("input[name='cutByMS']:checked").length == 0) {
    // For cutting by characters
    if (defCutTypeValue === 'letters') {
      // Check each document without individual options
      eltsWithoutIndividualOpts.forEach(function (elt) {
        // Needs warning...
        // If the number of characters-segment size/segment size-overlap size > 100
        if ((numChar[elt] - cutVal) / (cutVal - overVal) > maxSegs) {
          needsWarning = true
        }
      })
      // Do the same with words and lines
    }
    else if (defCutTypeValue === 'words') {
      eltsWithoutIndividualOpts.forEach(function (elt) {
        if ((numWord[elt] - cutVal) / (cutVal - overVal) > maxSegs) {
          needsWarning = true
        }
      })
    }
    else if (defCutTypeValue === 'lines') {
      eltsWithoutIndividualOpts.forEach(function (elt) {
        if ((numLine[elt] - cutVal) / (cutVal - overVal) > maxSegs) {
          needsWarning = true
        }
      })
      // If the segment size > 100 and there are documents without individual options
    }
    else if (cutVal > maxSegs && eltsWithoutIndividualOpts.length > 0) {
      needsWarning = true
    }
  }

  // needsWarning = true; // For testing
  if (needsWarning === true) {
    $('#needsWarning').val('true')
    const sizeWarning = `Current cut settings will result in over \ 
    100 new segments. Please be patient if you continue.`
    const footerButtons = `<button type="button" class="btn btn-default" id="warningContinue">Continue Anyway</button>
    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>`
    $('#warning-modal-footer').html(footerButtons)
    $('#warning-modal-message').html(sizeWarning)
    // Hide the processing icon and show the modal
    $('#status-prepare').css({ 'visibility': 'hidden' })
    $('#warning-modal').modal()
  }
  else {
    $('#needsWarning').val('false')
  }
}

let xhr

/**
 * Performs the ajax request.
 * @param {string} action
 */
function doAjax (action) {
  /* It's not really efficient to create a FormData and a json object,
     but the former is easier to pass to lexos.py functions, and the
     latter is easier for the ajax response to use. */
  const numActiveFiles = $('#numActiveFiles').val()
  const formData = new FormData($('form')[0])
  formData.append('action', action)
  const jsonForm = jsonifyForm()
  $.extend(jsonForm, { 'action': action })
  // Initiate a timer to allow user to cancel if processing takes too long
  const loadingTimeout = window.setTimeout(function () {
    $('#needsWarning').val('true')
    const timeWarning = `Lexos seems to be taking a long time.  \
    This may be because you are cutting a large number of documents. \ 
    If not, we suggest that you cancel, reload the page, and try again.`
    const footerButtons = `<button type="button" class="btn btn-default" data-dismiss="modal">Continue Anyway</button>
    <button type="button" class="btn btn-default" id="timerCancel" >Cancel</button>`
    $('#warning-modal-footer').html(footerButtons)
    $('#warning-modal-message').html(timeWarning)
    $('#warning-modal').modal()
  }, 10000) // 10 seconds
  xhr = $.ajax({
    url: '/doCutting',
    type: 'POST',
    processData: false, // important
    contentType: false,
    data: formData,
    error: function (jqXHR, textStatus, errorThrown) {
      $('#status-prepare').css({ 'visibility': 'hidden' })
      // Show an error if the user has not cancelled the action
      if (errorThrown !== 'abort') {
        const not_apply_msg = 'Lexos could not apply the cutting actions.'
        $('#error-modal-message').html(not_apply_msg)
        $('#error-modal').modal()
      }
      console.log(`bad: ${textStatus}: ${errorThrown}`)
    }
  }).done(function (response) {
    clearTimeout(loadingTimeout)
    $('#warning-modal').modal('hide') // Hide the warning if it is displayed
    response = JSON.parse(response)
    $('#preview-body').empty() // Correct
    $.each(response['data'], function () {
      const fileID = $(this)[0]
      const fileName = $(this)[1]
      const fileLabel = fileName
      const fileContents = $(this)[3]
      const indivCutButtons = `<a id="indivCutButtons_${fileID}" onclick="toggleIndivCutOptions(${fileID});" class="bttn indivCutButtons" role="button">Individual Options</a></legend>`
      // CSS truncates the document label
      const fieldSet = $(`<fieldSet class="individualpreviewwrapper"><legend class="individualpreviewlegend has-tooltip" style="color:#999; width:90%;margin: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${fileLabel} ${indivCutButtons}</fieldSet>`)
      const indCutOptsWrap = `<div id="indCutOptsWrap_${fileID}" class="cuttingoptionswrapper ind hidden">\
      <fieldSet class="cuttingoptionsfieldSet">\
      <legend class="individualcuttingoptionstitle">Individual Cutting Options</legend>\
      <div class="cuttingdiv individcut">\
      <div class="row">\
      <div class="col-md-5">\
      <label class="radio sizeradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndLetters_${fileID}" value="letters"/>\
      Characters/Segment</label>\
      </div>\
      <div class="col-md-7">\
      <label class="radio sizeradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndWords_${fileID}" value="words"/>\
      Tokens/Segment</label>\
      </div>\
      </div>\
      <div class="row cutting-radio">\
      <div class="col-md-5">\
      <label class="radio sizeradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndLines_${fileID}" value="lines"/>\
      Lines/Segment</label>\
      </div>\
      <div class="col-md-7">\
      <label class="radio numberradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndNumber_${fileID}" value="number"/>\
      Segments/Document</label>\
      </div>\
      </div>\
      </div>\
      <div class="row">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:3%;">\
      <label>\
      <span id="numOf${fileID}" class="cut-label-text">Number of Segments:</span>\
      <input type="number" min="1" step="1" name="cutValue_${fileID}" class="cut-text-input" id="individualCutValue" value=""/>\
      </label>\
      </div>\
      </div>\
      <div class="row overlap-div">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:3%;">\
      <label>Overlap: \
      <input type="number" min="0" name="cutOverlap_${fileID}" class="cut-text-input overlap-input" id="individualOverlap" value="0"/>\
      </label>\
      </div>\
      </div>\
      <div id="lastprop-div_${fileID}" class="row lastprop-div">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:1%;">\
      <label>Last Proportion Threshold: \
      <input type="number" min="0" id="cutLastProp_${fileID}" name="cutLastProp_${fileID}" class="cut-text-input lastprop-input" value="50" style="width:54px;margin-right:3px;"/>\
      %</label>\
      </div>\
      </div>\
      <div class="row">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:1%;">\
      <label>Cutset Label: \
      <input type="text" name="cutsetnaming_${fileID}" class="cutsetnaming" value="${fileName}" style="width:155px;display:inline; margin: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"/>\
      </label>\
      </div>\
      </div>\
      <div class="row cuttingdiv" id="cutByMSdiv">\
      <div class="col-sm-4">\
      <label>\
      <input type="checkbox" class="indivMS" name="cutByMS_${fileID}" id="cutByMS_${fileID}"/>\
      Cut by Milestone</label>\
      </div>\
      <div class="col-sm-8 pull-right" id="MSoptspan" style="display:none;">\
      <span>Cut document on this term \
      <input type="text" class="indivMSinput" name="MScutWord_${fileID}" id="MScutWord${fileID}" value="" style="margin-left:3px;width:130px;"/>\
      </span>\
      </div>\
      </div>\
      </fieldSet>\
      </div>`
      fieldSet.append(indCutOptsWrap)
      if ($.type(fileContents) === 'string') {
        fieldSet.append(`<div class="filecontents">${fileContents}</div>`) // Keep this with no whitespace!
      }
      else {
        $.each(fileContents, function (i, segment) {
          const segmentLabel = segment[0]
          const segmentString = segment[1]
          fieldSet.append(`<div class="filechunk"><span class="filechunklabel">${segmentLabel}</span><div>${segmentString}</div></div>`)
        })
      }
      $('#preview-body').append(fieldSet)
      // Hide the individual cutting wrapper if the form doesn't contain values for it
      if (!(`cutType_${fileID}` in formData) && formData[`cutType_${fileID}`] !== '') {
        $(`#indCutOptsWrap_${fileID}`).addClass('hidden')
      }
      // Check the cut type boxes
      if (formData['cutTypeInd'] === 'letters') {
        $(`#cutTypeIndLetters_${fileID}`).prop('checked', true)
      }
      if (formData['cutTypeInd'] === 'words') {
        $(`#cutTypeIndWords_${fileID}`).prop('checked', true)
      }
      if (formData['cutTypeInd'] === 'lines') {
        $(`#cutTypeIndLines_${fileID}`).prop('checked', true)
      }
      if (formData['cutTypeInd'] === 'number') {
        $(`#cutTypeIndNumber_${fileID}`).prop('checked', true)
        $(`#numOf_${fileID}`).html('Number of Segments')
        $('#lastprop-div').addClass('transparent')
        $(`#cutLastProp_${fileID}`).prop('disabled', true)
      }
      if (formData['Overlap']) { $(`#cutOverlap_${fileID}`).val(formData['Overlap']) } else { $(`#cutOverlap_${fileID}`).val(0) }
      if (formData[`cutLastProp_${fileID}`]) {
        $(`#lastprop-div_${fileID}`).val(formData[`#cutLastProp_${fileID}`])
      }
      if (formData['cutType'] === 'milestone') {
        $(`#cutTypeIndNumber_${fileID}`).prop('checked', true)
      }
      if (formData[`MScutWord_${fileID}`] === 'milestone') {
        $(`#MScutWord${fileID}`).val(formData['cuttingoptions']['cutValue'])
      }
    })
    $('.fa-folder-open-o').attr('data-original-title', `You have ${numActiveFiles} active document(s).`)
    $('#status-prepare').css({ 'visibility': 'hidden' })
  })
}


/**
 * Checks the form data for errors and warnings.
 * @param {string} action
 */
function process (action) {
  $('#status-prepare').css({ 'visibility': 'visible', 'z-index': '400000' })
  $('#formAction').val(action)
  $.when(checkForErrors()).done(function () {
    if ($('#hasErrors').val() === 'false') {
      checkForWarnings()
      $.when(checkForWarnings()).done(function () {
        if ($('#needsWarning').val() === 'false') {
          doAjax(action)
        }
      })
    }
  })
}

// Handle the Continue button in the warning modal
$(document).on('click', '#warningContinue', function () {
  $('#needsWarning').val('false')
  const action = $('#formAction').val()
  $('#warning-modal').modal('hide')
  doAjax(action)
  $('#status-prepare').css({ 'visibility': 'visible', 'z-index': '400000' })
})

// Handle the Timer Cancel button in the warning modal
$(document).on('click', '#timerCancel', function () {
  $('#needsWarning').val('false')
  $('#hasErrors').val('false')
  xhr.abort()
  $('#warning-modal-footer').append('<button>Moo</button>')
  $('#warning-modal').modal('hide')
  $('#status-prepare').css('visibility', 'hidden')
})


/**
 * Convert the form data into a JSON object.
 */
function jsonifyForm () {
  const form = {}
  $.each($('form').serializeArray(), function (i, field) {
    form[field.name] = field.value || ''
  })
  return form
}

/**
 * performs the download request (through flask)
 */
function downloadCutting () {
  // Unfortunately, you can't trigger a download with an ajax request; calling a
  // Flask route seems to be the easiest method.
    if ($('#num_active_files').val() > '0') {
        window.location = '/downloadCutting'
    }
}

$(function () {
  const msg = 'You have no active documents. Please activate \
  at least one document using the <a href="./manage">Manage</a> tool or\
  <a href="./upload">upload</a> a new document.'

  // When download, preview, or apply is clicked
  $('#action-buttons').click(function () {
      // check number of files
      if ($('#num_active_files').val() <  1) {
          // display error
          $('#error-modal-message').html(msg)
          $('#error-modal').modal()
      }
  })
  $('#actions').addClass('actions-cut')

  // Toggle cutting options when radio buttons with different classes are clicked
  const timeToToggle = 150
  $('.sizeradio').click(function () {
    const cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text')
    cuttingValueLabel.text('Segment Size:')

    $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
      .animate({ opacity: 1 }, timeToToggle)
      .find('.lastprop-input').prop('disabled', false)

    $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
      .animate({ opacity: 1 }, timeToToggle)
      .find('.overlap-input').prop('disabled', false)
  })

  $('.numberradio').click(function () {
    const cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text')
    cuttingValueLabel.text('Number of Segments:')

    $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
      .animate({ opacity: 0.2 }, timeToToggle)
      .find('.lastprop-input').prop('disabled', true)

    $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
      .animate({ opacity: 0.2 }, timeToToggle)
      .find('.overlap-input').prop('disabled', true)
  })

  // Toggle individual cut options on load
  $('.indivCutButtons').click(function () {
    const toggleDiv = $(this).closest('.individualpreviewwrapper').find('.cuttingoptionswrapper')
    toggleDiv.toggleClass('hidden')
    // slideToggle() only works if the div is first set to 'display:none'
    // toggleDiv.slideToggle(timeToToggle);
  })

  // Toggle milestone options
  function showMilestoneOptions () {
    if ($('#cutByMS').is(':checked')) {
      $('#MSoptspan').removeClass('hidden')
      $('#cuttingdiv').hide()
    }
    else {
      $('#MSoptspan').addClass('hidden')
      $('#cuttingdiv').show()
    }
  }

  $('#cutByMS').click(showMilestoneOptions)

  // showMilestoneOptions();

  $(document).on('click', '.indivMS', function () {
    showMilestoneOptions()
    if ($(this).is(':checked')) {
      $(this).parents('#cutByMSdiv').filter(':first').children('#MSoptspan').show()
      $(this).parents('#cutByMSdiv').filter(':first')
        .parents('.cuttingoptionswrapper').find('.individcut').hide()
    }
    else {
      $(this).parents('#cutByMSdiv').filter(':first').children('#MSoptspan').hide()
      $(this).parents('#cutByMSdiv').filter(':first')
        .parents('.cuttingoptionswrapper').find('.individcut').show()
    }
  })
})
