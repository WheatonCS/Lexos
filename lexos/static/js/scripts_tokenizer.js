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
function submissionError () {
    if ($('#num_active_files').val() < 1)
        return 'You must have at least one active document to proceed!'
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
function generateTokenizeResult () {
    // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    // convert form into an object map string to string
    const form = jsonifyForm()

    // the configuration for creating data table
    const dataTableConfig = {
        responsive: true,
        scrollX: true,
        // specify where the button is
        dom: '<\'row\'<\'col-sm-2\'l><\'col-sm-0 pull-right\'B>>' +
        '<\'row\'<\'col-sm-12\'tr>>' + '<\'row\'<\'col-sm-5\'i><\'col-sm-7\'p>>',

        // specify all the button that is put on to the page
        buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5'],

        fixedColumns: {
            leftColumns: 1
        }
    }

    // send the ajax request
    sendAjaxRequest('/tokenizeTable', form)
        .done(
            function (response) {
                const outerTableDivSelector = $('#tokenizeTable')
                // put the response onto the web page
                outerTableDivSelector.html(response)
                // initialize the data table
                outerTableDivSelector.children().DataTable(dataTableConfig)
                // display everything in the tokenize div.
                $('#tokenizeResult').css({'display': 'block'})
            })
        .fail(
            function (jqXHR, textStatus, errorThrown) {
                console.log('textStatus: ' + textStatus)
                console.log('errorThrown: ' + errorThrown)
                runModal('Error encountered while generating the tokenize table result.')
            })
        .always(
            function () {
                $('#status-analyze').css({'visibility': 'hidden'})
            })
}

$(function () {
    // Hide the tokenize result div.
    $('#tokenizeResult').css({'display': 'none'})

    /**
     * The event handler for generate tokenize clicked.
     */
    $('#get-tokenize').click(function () {
        // Get the possible error happened during submission the ajax call.
        const error = submissionError()

        if (error === null) {  // if there is no error
            generateTokenizeResult()
        }
        else {
            runModal(error)
        }
    })

})

