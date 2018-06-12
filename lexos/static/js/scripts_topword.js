$(function () {
  // define error message
  const msg = 'You do not have enough active documents. Please activate at \
  least two documents using the <a href="./manage">Manage</a> tool or \
  <a href="./upload">upload</a> a new document.'
  // When get topwords button is clicked
  $('#gettopword').click(function () {
      // Check number of active files
      if ($('#num_active_files').val() <  2) {
          //change button type to button so no request is made
          $("input[name='gen-topword']").prop("type", "button");
          // display error
          $('#error-modal .modal-body').html(msg)
          $('#error-modal').modal()
      }

  })

  //when download results is clicked
  $('#topworddownload').click(function () {
      // Check number of active files
      if ($('#num_active_files').val() <  2) {
          //change button type to button so no request is made
          $("input[name='gen-topword']").prop("type", "button");
          // display error
          $('#error-modal .modal-body').html(msg)
          $('#error-modal').modal()
      }

  })

  // Hide unnecessary div for DTM
  $('#normalize-options').css({ 'visibility': 'hidden' })
  // set the normalize option to raw count
  $("#normalizeTypeRaw").attr("checked", true)

  $('#temp-label-div').css('position', 'relative').css('left', '-6px').css('top', '0px')


  // display/hide expandable divs (Define Groups div) here
  function updateGroupOptionDiv() {
    $choice = $('.show-options div').siblings('input')
    $.each($choice, function () {
      if ($(this).is(':checked')) {
        $(this).siblings('div').show()
      } else { $(this).siblings('div').hide() }
    })
  }

  updateGroupOptionDiv()
  $('.groupOption-div').click(function () {
    updateGroupOptionDiv()
  })

  // Dynamically change the upper and lower bounds based on user inputs (Proportional Counts)
  $('#upperboundPC').click(function () {
    $(this).context.min = $('#lowerboundPC').val()
    $('#upperboundRC, #lowerboundRC').val(0)
  })

  $('#lowerboundPC').click(function () {
    $(this).context.max = $('#upperboundPC').val()
    $('#upperboundRC, #lowerboundRC').val(0)
  })

  // Reset proportional counts input fields while raw counts is chosed
  $('#upperboundRC, #lowerboundRC').click(function () {
    $('#upperboundPC, #lowerboundPC').val(0)
  })
})
