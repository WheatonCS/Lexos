/**
 * checks for errors
 */
const checkForErrors = function () {
    // Set Error and Warning Messages
    let errors = []
    // links to 404 so not working
    const err1 = 'You have no active documents. Please activate at least \
    one document using the \
    <a href=\"{{ url_for("manage") }}\">Manage</a> tool or \
    <a href=\"{{ url_for("upload") }}\">upload</a> a new document.'
    const err2 = 'You must provide a string to cut on.'
    const err3 = 'You must provide a default cutting value.'
    const err4 = 'Default cutting: Invalid segment size.'
    const err5 = 'Default cutting: Invalid overlap value.'
    const err6 = 'Individual cutting: Invalid segment size.'
    const err7 = 'Individual cutting: Invalid overlap value.'

    // Confirm that there are active files
    if ($('#num_active_files').val() === '0') {
        errors.push(err1)
    }

    // If cut by milestone is checked make sure there is a milestone value
    if ($('#cutByMS').is(':checked')) {
        if ($('#MScutWord').val() === '') {
            errors.push(err2)
        }
    }

    else {
        // Make sure there is a default cutting value
        const cutValues = $('#overallcutvalue')
        if (cutValues.val() === '') {
            errors.push(err3)
        }

        else {
            let overallcutvalueStr = cutValues.val()
            let overallcutvalue = parseInt(cutValues.val())
            let overallOverlapValue = parseInt($('#overallOverlapValue').val())
            let individualOverlap = parseInt($('#individualOverlap').val())
            let individualCutValueStr = cutValues.val()
            let individualCutValue = $('#individualCutValue').val()

            // Make sure the overall segment size not negative
            if (overallcutvalue !== Math.floor(overallcutvalue)) {
                errors.push(err4)
            }

            // Make sure the overall segment size not a decimal
            if (overallcutvalueStr !== Math.abs(overallcutvalue).toString()) {
                errors.push(err4)
            }

            // Make sure the overall segment size not 0
            if (overallcutvalue === 0) {
                errors.push(err4)
            }

            // Make sure the overall overlap is valid
            let overlap_check1 = (overallcutvalue <= overallOverlapValue)
            let overlap_check2 = Math.abs(Math.round(overallOverlapValue))
            let overlap_check2_con = (overlap_check2 !== overallOverlapValue)
            if (overlap_check1 || overlap_check2_con) {
                errors.push(err5)
            }

            // If there are individual segment cuts
            if (individualCutValue !== '') {
                individualCutValue = parseInt(individualCutValue)

                // Make sure the individual segment size not negative
                if (individualCutValue !== Math.floor(individualCutValue)) {
                    errors.push(err6)
                }

                // Make sure the individual segment size not a decimal
                const not_dec_check = Math.abs(individualCutValue).toString()
                if (individualCutValueStr !== not_dec_check) {
                    errors.push(err6)
                }

                // Make sure the individual segment size not 0
                if (individualCutValue === 0) {
                    errors.push(err6)
                }

                overlap_check1 = individualCutValue <= individualOverlap
                overlap_check2 = Math.abs(Math.round(individualOverlap))
                overlap_check2_con = (overlap_check2 !== individualOverlap)
                // Make sure the individual overlap is valid
                if (overlap_check1 || overlap_check2_con) {
                    errors.push(err7)
                }
            } // end if
        } // end else
    } // end else

    // if any errors load the first one into the error modal.
    if (errors.length > 0) {
        $('#hasErrors').val('true')
        $('#status-prepare').css({ 'visibility': 'hidden' })
        $('#error-modal-message').html(errors[0])
        $('#error-modal').modal()
    }

    else {
        $('#hasErrors').val('false')
    }
} // end checkForErrors

/**
 * checks whether the user needs a warning
 */
const checkForWarnings = function () {
    let needsWarning = false
    const maxSegs = 100
    let defCutTypeValue = $('input[name=\'cutType\']:checked').val() // Cut Type
    let cutVal = parseInt($('input[name=\'cutValue\']').val()) // Segment Size
    let overVal = parseInt($('#overallOverlapValue').val()) // Overlap Size
    let indivdivs = $('.cuttingoptionswrapper.ind') // All individual cutsets
    let eltswithoutindividualopts = [] // Elements without individual cutsets

    // Check each individual cutset
    needsWarning = indivdivs.each(checkIndividualCutset(maxSegs,
        defCutTypeValue, cutVal, overVal,
        indivdivs, eltswithoutindividualopts))

    if(needsWarning === false){
        needsWarning = checkMilestone(maxSegs, defCutTypeValue, cutVal,
            overVal, eltswithoutindividualopts)
    }



    // needsWarning = true; // For testing
    if (needsWarning === true) {
        $('#needsWarning').val('true')
        const sizeWarning = 'Current cut settings will result in over 100 \
        new segments. Please be patient if you continue.'
        const footerButtons = '<button type="button" class="btn btn-default" \
        id="warningContinue">Continue Anyway</button> <button type="button" \
        class="btn btn-default" data-dismiss="modal">Cancel</button>'
        $('#warning-modal-footer').html(footerButtons)
        $('#warning-modal-message').html(sizeWarning)
        // Hide the processing icon and show the modal
        $('#status-prepare').css({'visibility': 'hidden'})
        $('#warning-modal').modal()
    }

    else {
        $('#needsWarning').val('false')
    }
} // end checkForWarnings

/**
 * checks milestone for warnings
 * @param {number} maxSegs - maximum number of segments
 * @param {string} defCutTypeValue - cut type
 * @param {number} cutVal - segment size
 * @param {number} overVal - overlap size
 * @param {array} eltswithoutindividualopts - elements without cutsets
 * @returns {boolean}
 */
function checkMilestone (maxSegs, defCutTypeValue, cutVal,
                         overVal, eltswithoutindividualopts) {
    // If cut by milestone is checked
    if ($('input[name=\'cutByMS\']:checked').length === 0) {
        // For cutting by characters
        if (defCutTypeValue === 'letters') {
            // Check each document without individual options
            eltswithoutindividualopts.forEach(function (elt) {
                // Needs warning...
                // If the number of characters-segment size/segment size-overlap size > 100
                if ((numChar[elt] - cutVal) / (cutVal - overVal) > maxSegs) {
                    return true
                }
            })
            // Do the same with words and lines
        }
        else if (defCutTypeValue === 'words') {
            eltswithoutindividualopts.forEach(function (elt) {
                if ((numWord[elt] - cutVal) / (cutVal - overVal) > maxSegs) {
                    return true
                }
            })
        }
        else if (defCutTypeValue === 'lines') {
            eltswithoutindividualopts.forEach(function (elt) {
                if ((numLine[elt] - cutVal) / (cutVal - overVal) > maxSegs) {
                    return true
                }
            })
            // If the segment size > 100 and there are documents without individual options
        }
        else if (cutVal > maxSegs && eltswithoutindividualopts.length > 0) {
            return true
        }
    } // end if
    return false
} // end checkMilestone



/**
 * checks each individual cutset for warnings
 * @param {number} maxSegs - maximum number of segments
 * @param {string} defCutTypeValue - cut type
 * @param {number} cutVal - segment size
 * @param {number} overVal - overlap size
 * @param {array} indivdivs - all individual cutsets
 * @param {array} eltswithoutindividualopts - elements without cutsets
 * @returns {boolean}
 */
function checkIndividualCutset(maxSegs,defCutTypeValue, cutVal,
                         overVal, indivdivs, eltswithoutindividualopts) {
    let thisCutVal = $('#individualCutValue', this).val() // Individual segment size
    let thisOverVal = $('#individualOverlap', this).val() // Individual overlap size
    // Parse as integers
    if (thisCutVal !== '') {
        thisCutVal = parseInt(thisCutVal)
        thisOverVal = parseInt(thisOverVal)
    }

    // Get a list of each of the cutset indices
    let listindex = indivdivs.index(this)
    const currID = activeFileIDs[listindex] // activeFileIDs is defined in the template file
    let isCutByMS = $('.indivMS', this).is(':checked') // True if cut by milestone checked
    // If not cut by milestone and no segment size, add to no individual cutsets array
    if (!isCutByMS && thisCutVal === '') {
        eltswithoutindividualopts.push(listindex)
    }

    // If no segment size
    if (thisCutVal !== '') {
        // Get segment cut type
        const thisCutType =
            $('input[name=\'cutType_${currID}\']:checked').val()
            //$('input[name=\'cutType_' + currID + '\']:checked').val()
        // If not cut by milestone, use num_ variables set in template file
        if (!(isCutByMS)) {
            // Needs warning...
            // If the number of characters-overlap size/segment size-overlap size > 100
            const numCharSub = numChar[listindex] - thisOverVal
            const valSub = thisCutVal - thisOverVal
            const charDivVal = numCharSub/valSub
            const numWordSub = numWord[listindex] - thisOverVal
            const wordDivVal = numWordSub / valSub
            const numLineSub = numLine[listindex] - thisOverVal
            const lineDivVal = numLineSub / valSub
            const eltsLength = eltswithoutindividualopts.length
            if (thisCutType === 'letters' && (charDivVal) > maxSegs) {
                return true
            }
            // Same for segments and lines
            else if (thisCutType === 'words' && (wordDivVal) > maxSegs) {
                return true
            }
            else if (thisCutType === 'lines' && (lineDivVal) > maxSegs) {
                return true
                // Or if the segment size > 100
            }
            else if (thisCutVal > maxSegs && eltsLength > 0) {
                return true
            }
        } // end if
    } // end if
    return false
} // end checkIndividualCutset


let xhr

/**
 * performs the ajax request
 * @param {string} action - the type of action needed to be performed
 */
function doAjax (action) {
    /* It's not really efficient to create a FormData and a json object,
       but the former is easier to pass to lexos.py functions, and the
       latter is easier for the ajax response to use. */
    let formData = new FormData($('form')[0])
    formData.append('action', action)
    const jsonform = jsonifyForm()
    $.extend(jsonform, {'action': action})
    // Initiate a timer to allow user to cancel if processing takes too long
    const loadingTimeout = window.setTimeout(function () {
        $('#needsWarning').val('true')
        const timeWarning = 'Lexos seems to be taking a long time. This may \
        be because you are cutting a large number of documents. \
        If not, we suggest that you cancel, reload the page, and try again.'
        const footerButtons = '<button type="button" class="btn btn-default"\
        data-dismiss="modal">Continue Anyway</button>\
        <button type="button" class="btn btn-default" id="timerCancel" >\
        Cancel</button>'
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
            $('#status-prepare').css({'visibility': 'hidden'})
            // Show an error if the user has not cancelled the action
            if (errorThrown !== 'abort') {
                const cull_msg = 'Lexos could not apply the cutting actions.'
                $('#error-modal-message').html(cull_msg)
                $('#error-modal').modal()
            }
            console.log('bad: ' + textStatus + ': ' + errorThrown)
        }
    }).done(function (response) {
        clearTimeout(loadingTimeout)
        $('#warning-modal').modal('hide') // Hide the warning if it is displayed
        response = JSON.parse(response)
        $('#preview-body').empty() // Correct
        j = 0
        $.each(response['data'], function () {
            let fileID = $(this)[0]
            let filename = $(this)[1]
            let fileLabel = filename
            let fileContents = $(this)[3]
            const indivcutbuttons = '<a id="indivcutbuttons_' + fileID + '"\
            onclick="toggleIndivCutOptions(' + fileID + ');" \
            class="bttn indivcutbuttons" \
            role="button">Individual Options</a></legend>'

            // CSS truncates the document label
            const fieldsetSelector = '<fieldset \
            class="individualpreviewwrapper"><legend \
            class="individualpreviewlegend has-tooltip" \
            style="color:#999; width:90%;margin: auto; white-space: nowrap; \
            overflow: hidden; text-overflow: ellipsis;">\
            ' + fileLabel + ' ' + indivcutbuttons + '</fieldset>'

            let fieldset = $(fieldsetSelector)

            const indcutoptswrap = '<div \
            id="indcutoptswrap_' + fileID + '" \
            class="cuttingoptionswrapper ind hidden"><fieldset \
            class="cuttingoptionsfieldset"><legend \
            class="individualcuttingoptionstitle">Individual \
            Cutting Options</legend><div \
            class="cuttingdiv individcut"><div \
            class="row"><div \
            class="col-md-5"><label \
            class="radio sizeradio"><input \
            type="radio" \
            name="cutType_' + fileID + '" \
            id="cutTypeIndLetters_' + fileID + '" \
            value="letters"/>Characters/Segment</label></div><div \
            class="col-md-7"><label class="radio sizeradio">\
            <input type="radio" name="cutType_' + fileID + '" \
            id="cutTypeIndWords_' + fileID + '" \
            value="words"/>Tokens/Segment</label></div></div><div \
            class="row cutting-radio"><div class="col-md-5"><label \
            class="radio sizeradio"><input type="radio" \
            name="cutType_' + fileID + '" id="cutTypeIndLines_' + fileID + '" \
            value="lines"/>Lines/Segment</label></div><div \
            class="col-md-7"><label class="radio numberradio"><input \
            type="radio" name="cutType_' + fileID + '" \
            id="cutTypeIndNumber_' + fileID + '" \
            value="number"/>Segments/Document</label></div></div></div><div \
            class="row"><div class="col-md-6 pull-right" \
            style="padding-left:2px;padding-right:3%;"><label><span \
            id="numOf' + fileID + '" class="cut-label-text">Number of \
            Segments:</span><input type="number" min="1" step="1" \
            name="cutValue_' + fileID + '" class="cut-text-input" \
            id="individualCutValue" value=""/></label></div></div><div \
            class="row overlap-div"><div class="col-md-6 pull-right" \
            style="padding-left:2px;padding-right:3%;"><label>Overlap: \
            <input type="number" min="0" name="cutOverlap_' + fileID + '" \
            class="cut-text-input overlap-input" id="individualOverlap" \
            value="0"/></label></div></div>\
            <div id="lastprop-div_' + fileID + '" \
            class="row lastprop-div"><div class="col-md-6 pull-right" \
            style="padding-left:2px;padding-right:1%;"><label>Last Proportion \
            Threshold: <input type="number" min="0" \
            id="cutLastProp_' + fileID + '" \
            name="cutLastProp_' + fileID + '" \
            class="cut-text-input lastprop-input" value="50" \
            style="width:54px;margin-right:3px;"/> %</label></div></div><div \
            class="row"><div class="col-md-6 pull-right" \
            style="padding-left:2px;padding-right:1%;">\
            <label>Cutset Label: <input type="text" \
            name="cutsetnaming_' + fileID + '" class="cutsetnaming" \
            value="' + filename + '" style="width:155px;display:inline; \
            margin: auto; white-space: nowrap; overflow: hidden; \
            text-overflow: ellipsis;></label></div></div><div \
            class="row cuttingdiv" id="cutByMSdiv"><div \
            class="col-sm-4"><label><input type="checkbox" \
            class="indivMS" name="cutByMS_' + fileID + '" \
            id="cutByMS_' + fileID + '"/>Cut by Milestone</label></div><div \
            class="col-sm-8 pull-right" id="MSoptspan" \
            style="display:none;"><span>Cut document on this term \
            <input type="text" class="indivMSinput" \
            name="MScutWord_' + fileID + '" id="MScutWord' + fileID + '" \
            value="" \
            style="margin-left:3px;width:130px;"/></span></div>\
            </div></fieldset></div>'

            fieldset.append(indcutoptswrap)
            if ($.type(fileContents) === 'string') {
                j++
                const fieldsetAppend1 = '<div\
                class="filecontents">' + fileContents + '</div>'
                fieldset.append(fieldsetAppend1) // Keep this with no whitespace!
            } else {
                $.each(fileContents, function (i, segment) {
                    j++
                    const segmentLabel = segment[0]
                    const segmentString = segment[1]
                    const fieldsetAppend2 = '<div class="filechunk"><span \
                    class="filechunklabel">' + segmentLabel + '</span>\
                    <div>' + segmentString + '</div></div>'
                    fieldset.append(fieldsetAppend2)
                })
            }
            $('#preview-body').append(fieldset)
            // Hide the individual cutting wrapper if the form doesn't contain values for it
            const cutTypeID = 'cutType_' + fileID
            if (!(cutTypeID in formData) && formData[cutTypeID] !== '') {
                $('#indcutoptswrap_' + fileID).addClass('hidden')
            }
            // Check the cut type boxes
            if (formData['cutTypeInd'] === 'letters') {
                $('#cutTypeIndLetters_' + fileID).prop('checked', true)
            }
            if (formData['cutTypeInd'] === 'words') {
                $('#cutTypeIndWords_' + fileID).prop('checked', true)
            }
            if (formData['cutTypeInd'] === 'lines') {
                $('#cutTypeIndLines_' + fileID).prop('checked', true)
            }
            if (formData['cutTypeInd'] === 'number') {
                $('#cutTypeIndNumber_' + fileID).prop('checked', true)
                $('#numOf_' + fileID).html('Number of Segments')
                $('#lastprop-div').addClass('transparent')
                $('#cutLastProp_' + fileID).prop('disabled', true)
            }
            if (formData['Overlap']) {
                $('#cutOverlap_' + fileID).val(formData['Overlap'])
            }
            else {
                $('#cutOverlap_' + fileID).val(0)
            }
            if (formData['cutLastProp_' + fileID]) {
                const lastPropID = '#lastprop-div_' + fileID
                $(lastPropID).val(formData['#cutLastProp_' + fileID])
            }
            if (formData['cutType'] === 'milestone') {
                $('#cutTypeIndNumber_' + fileID).prop('checked', true)
            }
            if (formData['MScutWord_' + fileID] === 'milestone') {
                const MScutID = '#MScutWord' + fileID
                $(MScutID).val(formData['cuttingoptions']['cutValue'])
            }
        })
        const documentNum = 'You have ' + j + ' active document(s).'
        $('.fa-folder-open-o').attr('data-original-title', documentNum)
        $('#status-prepare').css({'visibility': 'hidden'})
    })
} // end doAjax

// Function to check the form data for errors and warnings
/**
 * checks the form data for errors and warnings
 * @param {string} action
 */
function process (action) {
    $('#status-prepare').css({'visibility': 'visible', 'z-index': '400000'})
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
} // end process

//==Warning Modal Click Functions=================
// Handle the Continue button in the warning modal
$(document).on('click', '#warningContinue', function () {
    $('#needsWarning').val('false')
    let action = $('#formAction').val()
    $('#warning-modal').modal('hide')
    doAjax(action)
    $('#status-prepare').css({'visibility': 'visible', 'z-index': '400000'})
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
//=====================================================

/**
 *  converts the form data into a JSON object
 */
function jsonifyForm () {
    let form = {}
    $.each($('form').serializeArray(), function (i, field) {
        form[field.name] = field.value || ''
    })
    return form
} // end jsonifyForm

/**
 * calls a flask route to trigger a download
 */
function downloadCutting () {
    // Unfortunately, you can't trigger a download with an ajax request; calling a
    // Flask route seems to be the easiest method.
    window.location = '/downloadCutting'
} // end downloadCutting

$(function () {
    $('#actions').addClass('actions-cut')

    // Toggle cutting options when radio buttons with different classes are clicked
    const timeToToggle = 150
    $('.sizeradio').click(function () {
        let cuttingValueLabel =
            $(this).parents('.cuttingoptionswrapper').find('.cut-label-text')
        cuttingValueLabel.text('Segment Size:')

        $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
            .animate({opacity: 1}, timeToToggle)
            .find('.lastprop-input').prop('disabled', false)

        $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
            .animate({opacity: 1}, timeToToggle)
            .find('.overlap-input').prop('disabled', false)
    })

    $('.numberradio').click(function () {
        let cuttingValueLabel =
            $(this).parents('.cuttingoptionswrapper').find('.cut-label-text')
        cuttingValueLabel.text('Number of Segments:')

        $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
            .animate({opacity: 0.2}, timeToToggle)
            .find('.lastprop-input').prop('disabled', true)

        $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
            .animate({opacity: 0.2}, timeToToggle)
            .find('.overlap-input').prop('disabled', true)
    })

    // Toggle individual cut options on load
    $('.indivcutbuttons').click(function () {
        let toggleDiv =
            $(this).closest('.individualpreviewwrapper')
                .find('.cuttingoptionswrapper')
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
            $(this).parents('#cutByMSdiv').filter(':first')
                .children('#MSoptspan').show()
            $(this).parents('#cutByMSdiv').filter(':first')
                .parents('.cuttingoptionswrapper').find('.individcut').hide()
        }
        else {
            $(this).parents('#cutByMSdiv').filter(':first')
                .children('#MSoptspan').hide()
            $(this).parents('#cutByMSdiv').filter(':first')
                .parents('.cuttingoptionswrapper').find('.individcut').show()
        }
    })
})

