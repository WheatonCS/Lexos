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
    const active_file_num_too_few_err = 'You do not have enough active documents. Please activate at least two documents using the <a href="./manage">Manage</a> tool or <a href="./upload">upload</a> a new document.'
    if ($('#num_active_files').val() < 2)
        return active_file_num_too_few_err
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
function generateSimResult () {
    // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    // convert form into an object map string to string
    const form = jsonifyForm()

    // the configuration for creating data table
    const dataTableConfig = {
        // do not display pages
        paging: false,

        // specify where the button is
        dom: '<\'row\'<\'col-sm-2\'l><\'col-sm-3 pull-right\'B>>' +
        '<\'row\'<\'col-sm-12\'tr>>' + '<\'row\'<\'col-sm-5\'i><\'col-sm-7\'p>>',

        // specify all the button that is put on to the page
        buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5']
    }

    // send the ajax request
    sendAjaxRequest('/similarityHTML', form)
        .done(
            function (response) {
                const outerTableDivSelector = $('#simTable')
                // put the response onto the web page
                outerTableDivSelector.html(response)
                // initialize the data table
                outerTableDivSelector.children().DataTable(dataTableConfig)
                // display the similarity result
                $('#similaritiesResults').css({'display': 'block'})  // display everything
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

$(function () {

    // hide the similarity
    $('#similaritiesResults').css({'display': 'none'})

    /**
     * The event handler for generate similarity clicked
     */
    $('#get-sims').on('click', function () {
        const error = submissionError()  // the error happens during submission

        if (error === null) {  // if there is no error
            generateSimResult()
        }
        else {
            runModal(error)
        }
    })

})

