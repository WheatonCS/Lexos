/**
 * the function to run the error modal
 * @param htmlMsg {string} - the message to display, you can put html in it
 */
function runModal (htmlMsg) {
    $('#error-modal-message').html(htmlMsg)
    $('#error-modal').modal()
}

/**
 * check all the easy error with js, in this case, one document is required
 * @returns {string | null} the errors that is checked by JS, if there is no error the result will be null
 */
function submissionError () {
    if ($('#num_active_files').val() < 1)
        return 'You must have at least 1 active documents to proceed!'
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
function generateStatsFileResult () {
    // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    // convert form into an object map string to string
    const form = jsonifyForm()

    // the configuration for creating data table
    const dataTableConfig = {
        // specify all the button that is put on to the page
        buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5']
    }

    // send the ajax request
    sendAjaxRequest('/statsFile', form)
        .done(
            function (response) {
                const outerTableDivSelector = $('#file-table')
                // put the response onto the web page
                outerTableDivSelector.html(response)
                // initialize the data table
                outerTableDivSelector.children().DataTable(dataTableConfig)
                // display the similarity result
                $('#stats-result').css({'display': 'block'})  // display everything
            })
        .fail(
            function (jqXHR, textStatus, errorThrown) {
                console.log('textStatus: ' + textStatus)
                console.log('errorThrown: ' + errorThrown)
                runModal('error encountered while generating the statistics result.')
            })
        .always(
            function () {
                $('#status-analyze').css({'visibility': 'hidden'})
            })
}

/**
 * display the result of the similarity query on web page
 */
function generateStatsBoxPlot () {
    // show loading icon
    $('#status-analyze').css({'visibility': 'visible'})

    // convert form into an object map string to string
    const form = jsonifyForm()

    // send the ajax request
    sendAjaxRequest('/statsBoxPlot', form)
        .done(
            function (response) {
                $('#box-plot').html(response)
            })
        .fail(
            function (jqXHR, textStatus, errorThrown) {
                console.log('textStatus: ' + textStatus)
                console.log('errorThrown: ' + errorThrown)
                runModal('error encountered while generating the statistics result.')
            })
        .always(
            function () {
                $('#status-analyze').css({'visibility': 'hidden'})
            })
}

$(function () {
    // hide the normalize options and set it to raw count.
    $('#normalize-options').css({'visibility': 'hidden'})
    $('#normalizeTypeRaw').attr('checked', true)

    // Reset the maximum number of documents when a checkbox is clicked
    $('.minifilepreview').click(function () {
        $('#cullnumber').attr('max', $('.minifilepreview:checked').length)
    })

    // Toggle file selection & reset the maximum number of documents when 'Toggle All' is clicked
    $('#allCheckBoxSelector').click(function () {
        if (this.checked) {
            $('.minifilepreview:not(:checked)').trigger('click')
            $('#cullnumber').attr('max', $('.minifilepreview:checked').length)
        } else {
            $('.minifilepreview:checked').trigger('click')
            $('#cullnumber').attr('max', '0')
        }
    })

    // hide the stats result div.
    $('#stats-result').css({'display': 'none'})

    /**
     * The event handler for generate statistics clicked
     */
    $('#get-stats').click(function () {
        const error = submissionError()  // the error happens during submission

        if (error === null) {  // if there is no error
            generateStatsFileResult()
            generateStatsBoxPlot()
        }
        else {
            runModal(error)
        }
    })

})

