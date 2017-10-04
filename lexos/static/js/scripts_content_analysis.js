/**
 * Created by alvaro on 9/23/17.
 */
function analyzeContent(action) {
  if ($('#num_active_files').val() == '0') {
    $('#error-modal').modal();
    return
  }

  $('#status-prepare').css({ 'visibility': 'visible' });

  $('#formAction').val(action);
  var formData = new FormData($('form')[0]);

  $.ajax({
    url: '/contentanalysis',
    type: 'POST',
    processData: false, // important
    contentType: false, // important
    data:  $('form').serialize(),
    error: function (jqXHR, textStatus, errorThrown) {
      $('#error-modal-message').html('Lexos could not apply the analysis content actions.');
      $('#error-modal').modal();
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    }
  }).done(function (response) {
    response = JSON.parse(response);
    $('#preview-body').empty();
    $.each(response['data'], function (i, item) {
      table = response['data'];
      dict_labels = response['dictionary_labels'];
      $('#table').empty();
      $('#table').append(table);

      $('#dictionaries').empty();
      for (i = 0; i < dict_labels.length; i++) {
          html = "<input type='button' value='" +
              dict_labels[i] + "'" +
              "onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";

          $('#dictionaries').append(html);
      }
      $('#status-prepare').css({ 'visibility': 'hidden' })
    })
  })
}
function upload_dictionaries(action) {
  if ($('#num_active_files').val() == '0') {
    $('#error-modal').modal();
    return
  }

  $('#status-prepare').css({ 'visibility': 'visible' });

  $('#formAction').val(action);
  var formData = new FormData($('form')[0]);

  $.ajax({
    url: '/uploaddictionaries',
    type: 'POST',
    processData: false, // important
    contentType: false, // important
    data: formData,
    error: function (jqXHR, textStatus, errorThrown) {
      $('#error-modal-message').html('Lexos could not apply the analysis content actions.');
      $('#error-modal').modal();
      console.log('bad: ' + textStatus + ': ' + errorThrown)
    }
  }).done(function (response) {
    response = JSON.parse(response);
    $('#preview-body').empty();
    $.each(response['dictionary_labels'], function (i, item) {
      dict_labels = response['dictionary_labels'];
      $('#dictionaries').empty();
      for (i = 0; i < dict_labels.length; i++) {
          html = "<input type='button' value='" +
              dict_labels[i] + "'" +
              "onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";
          $('#dictionaries').append(html);
      }
      $('#status-prepare').css({ 'visibility': 'hidden' })
    })
  })
}
$(function() {
    $('#save_formula').on('click', function(){
        var calc_input = $("input[name=display]").val();
       var data = JSON.stringify({"calc_input": calc_input});
       $.ajax({
          url: "/saveformula",
          type: "POST",
          data: data,
          contentType: 'application/json;charset=UTF-8'
        });
      });
 });
function backspace(calc){
    var length = calc.display.value.length;
    calc.display.value=calc.display.value.substring(0,length-1);
}
