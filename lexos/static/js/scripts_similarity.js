/**
 * the function to run the error modal
 * @param htmlMsg {string} - the message to display, you can put html in it
 */
function runModal (htmlMsg) {
    $('#error-modal-message').html(htmlMsg)
    $('#error-modal').modal()
}


/**
 * check all the easy error with js, in this case, you need more than 2 documents
 * @returns {string | null} the errors that is checked by JS, if there is no error the result will be null
 */
function submissionError() {
    if ($('#num_active_files').val() < 2)
        return "You must have at least 2 active documents to proceed!"
    else
        return null
}

/**
 * the function to convert the from into json
 * @returns {{string: string}} - the from converted to json
 */
function jsonifyForm () {
    const form = {}
    $.each($('form').serializeArray(), function (i, field) {
        form[field.name] = field.value || ''
    })
    return form
}


/**
 * send the ajax request
 * @param url: the url to post
 * @param form: the form data packed into an object
 * @returns {jQuery.Ajax}: an jQuery Ajax object
 */
function sendAjaxRequest (url, form) {
    return $.ajax({
        type: 'POST',
        url: url,
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(form)
    })

}

/**
 * display the result of the similarity query on web page
 */
function displaySimResult () {
        // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    // convert form into an object map string to string
    const form = jsonifyForm()

    // send the ajax request
    sendAjaxRequest("/similarityHTML", form)
        .done(
            function (response) {
                const outerTableDivSelector = $('#simTable')
                outerTableDivSelector.html(response)  // put the response into the web page
                outerTableDivSelector.children().DataTable({  // init the response table to data table
                    paging: false,  // no page
                })
                $('#similaritiesResults').css({"display": "block"})  // display everything
            })
        .fail(
            function (jqXHR, textStatus, errorThrown) {
                console.log('textStatus: ' + textStatus)
                console.log('errorThrown: ' + errorThrown)
                runModal('error encountered while generating the similarity query result.')
            })
        .always(
            function () {
                $('#status-analyze').css({'visibility': 'hidden'})
            })
}

/**
 * download the sim csv
 */
function downloadSimCsv () {
        // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    // convert form into an object map string to string
    const form = jsonifyForm()

    // send the ajax request
    sendAjaxRequest("/similarityCSV", form)
        .fail(
            function (jqXHR, textStatus, errorThrown) {
                console.log('textStatus: ' + textStatus)
                console.log('errorThrown: ' + errorThrown)
                runModal('error encountered while generating the similarity query result.')
            })
        .always(
            function () {
                $('#status-analyze').css({'visibility': 'hidden'})
            })
}


$(function () {

    // hide the similarity
    $("#similaritiesResults").css({"display": "none"})

    $('#get-sims').click(function () {
        const error = submissionError()  // the error happens during submission

        if (error === null) {  // if there is no error
            displaySimResult()
        }
        else {
            runModal(error)
        }
    })

    $("#sims-download").click(function () {
        const error = submissionError()  // the error happens during submission

        if (error === null) {  // if there is no error
            downloadSimCsv()
        }
        else {
            runModal(error)
        }

    })
})

