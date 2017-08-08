/* #### INITIATE SCRIPTS ON $(DOCUMENT).READY() #### */
$(document).ready(function () {
  // Hide unnecessary divs for DTM
  var newLabelsLocation = $('#normalize-options').parent()
  var newNormalizeLocation = $('#temp-label-div').parent()
  var tempNormalize = $('#normalize-options').html()
  var tempLabels = $('#temp-label-div').html()
  $('#normalize-options').remove()
  $('#temp-label-div').remove()
  newLabels = $('<fieldset class="analyze-advanced-options" id="temp-label-div"></fieldset>').append(tempLabels)
  newNormalize = $('<fieldset class="analyze-advanced-options" id="normalize-options"></fieldset>').append(tempNormalize)
  newLabelsLocation.append(newLabels)
  newNormalizeLocation.append(newNormalize)
  $('#normalize-options').hide()

  // $("#normalize-options").css({"visibility":"hidden"});

  // Reset the maximum number of documents when a checkbox is clicked
  /*	$("#cullnumber").change(function() {
      if ($("#cullnumber").val() > $(".minifilepreview:checked").length) {
        alert('blah');
      }
    }); */

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

  /* #### INITIATE MAIN DATATABLE #### */
  //* Change the element name and test whether the table variable persists
  table = $('#statstable').DataTable({
    'scrollY': '370px', // Table max-height
    'scrollCollapse': true, // Collapse shorter
    // Change DataTable default language
    'language': {
      'lengthMenu': 'Display _MENU_ documents',
      'info': 'Showing _START_ to _END_ of _TOTAL_ documents'
    },
    // Main column definitions
    //* May need to make the index sortable.
    //* Need to modify natural sorting to be case insensitive.
    'columnDefs': [
      { sortable: true, targets: '_all' },
      { type: 'natural', targets: '_all' }
    ],
    'ordering': true,
    'searching': true,
    'paging': true,
    'pagingType': 'full_numbers',
    'pageLength': 10,
    'lengthMenu': [[10, 25, 50, -1], [10, 25, 50, 'All']],
    'dom': "<'row'<'col-sm-6'l><'col-sm-6 to-right'B>>" +
    "<'row'<'col-sm-12'tr>>" +
    "<'row'<'col-sm-5'i><'col-sm-7'p>>",
    'buttons': [
      'copyHtml5',
      'excelHtml5',
      'csvHtml5',
      {
        extend: 'csvHtml5',
        text: 'TSV',
        fieldSeparator: '\t',
        extension: '.tsv'
      },
      'pdfHtml5'
    ]
  })
})
