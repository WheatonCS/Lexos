// Function to convert the form data into a JSON object
function jsonifyForm () {
    var form = {}
    $.each($('form').serializeArray(), function (i, field) {
        form[field.name] = field.value || ''
    })
    return form
}

function doAjax (action) {
    var form = jsonifyForm()
    var extension = {}
    extension[action] = true
    $.extend(form, extension)
    $.ajax({
            'type': 'POST',
            'url': '/dendrogramDiv',
            'contentType': 'application/json; charset=utf-8',
            'dataType': 'json',
            'data': JSON.stringify(form),
            'complete': function (response) {
                $('#dendrogram-result').html(response.responseText)
            },
            'error': function (error) {
                $('#error-modal').html('Server Failed to Plot the Dendrogram')
            }
        }
    )
}

function submissionError () {
    const err = 'A dendrogram requires at least 2 active documents to be created.'
    const activeFiles = $('#num_active_files').val()
    if (activeFiles < 2)
        return err
    else
        return null
}

$(document).ready(function () {

    // Events after 'Get Dendrogram' is clicked, handle exceptions
    $('#getdendro, #dendroPDFdownload, #dendroSVGdownload, #dendroPNGdownload, #download').on('click', function () {

        const action = $(this).attr('id')  // the action name of the ajax request
        const error = submissionError()  // the error happens during submission

        if (error === null) {  // if there is no error
            doAjax(action)
        }
        else {
            const modal = $('#error-modal')
            modal.html(error)
            modal.modal()
        }
    })

})
