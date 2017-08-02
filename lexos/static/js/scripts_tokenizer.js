$(function () {
  // Toggle the additional DTM contents option
  function updateCSVcontentOption () {
    if ($('#greyword').is(':checked') || $('#culling').is(':checked') || $('#MFW').is(':checked')) {
      $('#csvcontdiv').show()
    } else {
      $('#csvcontdiv').hide()
    }
  }

  updateCSVcontentOption()

  $('#culling-options').click(function () {
    updateCSVcontentOption()
  })

  $('#csvgen').click(function () {
    $('#status-analyze').css({ 'visibility': 'visible', 'z-index': '400000' })
  })
})
