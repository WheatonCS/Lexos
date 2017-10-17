/**
 * the function to convert the from into json
 * @returns {{string: string}} - the from converted to json
 */
function jsonifyForm () {
    var form = {}
    $.each($('form').serializeArray(), function (i, field) {
        form[field.name] = field.value || ''
    })
    return form
}

/**
 * the function to run the error modal
 * @param htmlMsg {string} - the message to display, you can put html in it
 */
function runModal (htmlMsg) {
    $('#error-modal-message').html(htmlMsg)
    $('#error-modal').modal()
}

/**
 * the function to do ajax in dendrogram
 * @param url {string} - the url to do post
 * @param extension {string | null} - used to download dendrogram, to specify the file type to download. if unused, this will be null
 */
function doAjax (url, extension) {
    // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    var form = jsonifyForm()
    $.extend(form, {downloadFileExtension: extension})
    $.ajax({
            type: 'POST',
            url: url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: JSON.stringify(form),
            complete: function (response) {
                $('#status-analyze').css({'visibility': 'hidden'})
                $('#dendrogram-result').html(response['responseJSON']['dendroDiv'])
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log('textStatus: ' + textStatus)
                console.log('errorThrown: ' + errorThrown)
                runModal('backend fail to plot the dendrogram.')
            }
        }
    )
}

/**
 * the error message for the submission
 * @returns {string | null} - if it is null, it means no error, else then the string is the error message
 */
function submissionError () {
    const err = 'A dendrogram requires at least 2 active documents to be created.'
    const activeFiles = $('#num_active_files').val()
    if (activeFiles < 2)
        return err
    else
        return null
}

/**
 * When the HTML documents finish loading
 */
$(document).ready(function () {

    /**
     * the events after dendrogram is clicked
     */
    $('#getdendro').on('click', function () {
        const error = submissionError()  // the error happens during submission

        if (error === null) {  // if there is no error
            doAjax('/dendrogramDiv', null)
        }
        else {
            runModal(error)
        }

    })

    /**
     * The events after any download button is clicked
     */
    $('.dendroDownload').on('click', function () {

        const error = submissionError()  // the error happens during submission
        const fileExtension = $(this).attr('data-file-extension')  // the file extension

        if (error === null) { // if there is no error
            doAjax('/dendrogramDownload', fileExtension)
        }
        else {
            runModal(error)
        }
    })

})
