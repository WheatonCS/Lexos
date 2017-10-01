/**
 * Created by alvaro on 9/23/17.
 */
function analyzeContent(action) {
  if ($('#num_active_files').val() == '0') {
    $('#error-modal').modal()
    return
  }

  $('#status-prepare').css({ 'visibility': 'visible' })

  $('#formAction').val(action)
  var formData = new FormData($('form')[0])

  $.ajax({
    url: '/contentanalysis',
    type: 'POST',
    processData: false, // important
    contentType: false, // important
    data: formData,
    error: function (jqXHR, textStatus, errorThrown) {
      $('#error-modal-message').html('Lexos could not apply the scrubbing actions.')
      $('#error-modal').modal()
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    }
  }).done(function (response) {
    response = JSON.parse(response)
    $('#preview-body').empty()
    $.each(response['data'], function (i, item) {
      table = response['data']
        fileID = $(this)[0]
      filename = $(this)[1]
      fileLabel = $(this)[2]
      fileContents = $(this)[3]
      fieldset = $('<fieldset></fieldset>')
      // CSS truncates the document name
      fieldset.append('<legend class="has-tooltip" style="color:#999; width:90%;margin: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + filename + '</legend>')
      fieldset.append('<div class="filecontents">' + fileContents + '</div>') // Keep this with no whitespace!
      $('#preview-body').append(table)
      $('#status-prepare').css({ 'visibility': 'hidden' })
    })
  })
}
