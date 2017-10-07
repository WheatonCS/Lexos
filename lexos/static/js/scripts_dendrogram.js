$(document).ready(function () {

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
                }
            }
        )
    }

    // Events after 'Get Dendrogram' is clicked, handle exceptions
    $('#getdendro, #dendroPDFdownload, #dendroSVGdownload, #dendroPNGdownload, #download').on('click', function () {
        const err = 'A dendrogram requires at least 2 active documents to be created.'
        const activeFiles = $('#num_active_files').val()
        const action = $(this).attr('id')

        if (activeFiles < 2) {
            $('#status-analyze').css({'visibility': 'hidden'})
            $('#error-modal-message').html(err)
            $('#error-modal').modal()
        } else if (action === 'getdendro') {
            doAjax('getdendro')
        }

    })

})
