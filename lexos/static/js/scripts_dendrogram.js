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
                'url': '/cluster',
                'contentType': 'application/json; charset=utf-8',
                'dataType': 'json',
                'data': JSON.stringify(form),
                'complete': function (response) {
                    $('#pdf').attr('src', '/dendrogramimage?' + response['responseJSON']['ver'])
                    document.getElementById('graph-anchor').scrollIntoView({
                        block: 'start',
                        behavior: 'smooth'
                    })
                    $('#status-analyze').css({'visibility': 'hidden'})
                }
            }
        )
    }

    // Events after 'Get Dendrogram' is clicked, handle exceptions
    $('#getdendro, #dendroPDFdownload, #dendroSVGdownload, #dendroPNGdownload, #download').on('click', function () {
        var err1 = 'A dendrogram requires at least 2 active documents to be created.'
        var activeFiles = $('#num_active_files').val()

        if (activeFiles < 2) {
            $('#status-analyze').css({'visibility': 'hidden'})
            $('#error-modal-message').html(err1)
            $('#error-modal').modal()
        }
    })

    // Calculate the threshold values based on criterions
    var inconsistentrange = '0 ≤ t ≤ '
    var maxclustRange = '2 ≤ t ≤ '
    var range = ' ≤ t ≤ '

    var inconsistentMaxStr = inconsistentMax.toString()
    var maxclustMaxStr = maxclustMax.toString()
    var distanceMaxStr = distanceMax.toString()
    var monocritMaxStr = monocritMax.toString()

    var distanceMinStr = distanceMin.toString()
    var monocritMinStr = monocritMin.toString()

    var inconsistentOp = inconsistentrange.concat(inconsistentMaxStr)
    var maxclustOp = maxclustRange.concat(maxclustMaxStr)
    var distanceOp = distanceMinStr.concat(range, distanceMaxStr)
    var monocritOp = monocritMinStr.concat(range, monocritMaxStr)

    var placeholderText = {
        'Inconsistent': inconsistentOp,
        'Maxclust': maxclustOp,
        'Distance': distanceOp,
        'Monocrit': monocritOp
    }

    $('#criterion').on('change', function () {
        var selectedVal = $('#criterion').find(':selected').text()
        $('#threshold').attr('placeholder', placeholderText[selectedVal])
    }).on('click', function () {
        var selectedVal = $('#criterion').find(':selected').text()
        $('#threshold').attr('placeholder', placeholderText[selectedVal])
    })
})
