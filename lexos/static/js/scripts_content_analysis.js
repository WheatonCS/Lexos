/**
 * Created by alvaro on 9/23/17.
 */
$(function() {
    $('#analyze_button').on('click', function(){
        var calc_input = $("input[name=display]").val();
       var data = JSON.stringify({"calc_input": calc_input});
       $.ajax({
          url: "/contentanalysis",
          type: "POST",
          data: data,
          contentType: 'application/json;charset=UTF-8'
        }).done(function (response) {
            response = JSON.parse(response);
            $('#preview-body').empty();
            $.each(response['data'], function (i, item) {
                var table = response['data'];
                var dict_labels = response['dictionary_labels'];
                $('#table').empty();
                $('#table').append(table);
                $('#dictionaries').empty();
                for (i = 0; i < dict_labels.length; i++) {
                    var html = "<input type='button' value='" +
                        dict_labels[i] + "'" +
                        " onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";
                    $('#dictionaries').append(html);
                }
                $('#status-prepare').css({'visibility': 'hidden'})
            })
        });
      });
 });
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
          var dict_labels = response['dictionary_labels'];
          var active_dicts = response['active_dictionaries'];
          $('#dictionaryButtons').empty();
          $('#checkboxes').empty();
          for (i = 0; i < dict_labels.length; i++) {
              var buttons = "<input type='button' value='" + dict_labels[i] + "'" +
                  "onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";
              $('#dictionaryButtons').append(buttons);
              var checkboxes = "<form method='POST'>" +
                  "<input type='hidden' name='dictionary' value='"+dict_labels[i]+"'>" +
                   "<input type='checkbox' id='dict_checkbox' onclick='toggle_checkbox("+i+")' ";
              if(active_dicts[i]){
                  checkboxes += " checked";
              }
              checkboxes += ">"+dict_labels[i]+ "</form>";
              $('#checkboxes').append(checkboxes);
          }
          $('#status-prepare').css({ 'visibility': 'hidden' });
        })
    })
}
function toggle_checkbox(i) {
    var dict_names = [];
    $("input[name=dictionary]").each(function(){ dict_names.push(this.value); });
        var dict_name = dict_names[i];
       var data = JSON.stringify({"dict_name": dict_name});
       $.ajax({
          url: "/toggledictionary",
          type: "POST",
          data: data,
          contentType: 'application/json;charset=UTF-8'
       }).done(function (response) {
           response = JSON.parse(response);
           var dict_labels = response['dictionary_labels'];
           var active_dicts = response['active_dictionaries'];
           $('#dictionaryButtons').empty();
           $('#checkboxes').empty();
           $('#display').val("");
      for (var i = 0; i < dict_labels.length; i++) {
          if(active_dicts[i]) {
              var buttons = "<input type='button' value='" + dict_labels[i] + "'" +
                  " onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";
              $('#dictionaryButtons').append(buttons);
          }
          var checkboxes = "<form method='POST'>" +
              "<input type='hidden' name='dictionary' value='"+dict_labels[i]+"'>" +
               "<input type='checkbox' id='dict_checkbox' onclick='toggle_checkbox("+i+")' ";
          if(active_dicts[i]){
              checkboxes += " checked";
          }
          checkboxes += ">"+dict_labels[i]+ "</form>";
          $('#checkboxes').append(checkboxes);
      }
    })
}
function backspace(calc){
    var content = calc.display.value;
    var length = content.length;
    if(content[length -1] == "]"){
        content = content.substring(0,content.lastIndexOf("["));
    }
    else if(content.endsWith("sin(") || content.endsWith("cos(") ||
            content.endsWith("tan(") || content.endsWith("log(")){
        content = content.substring(0,length - 4);
    }
    else if(content.endsWith("^(") || content.endsWith("√(") ){
        content = content.substring(0,length - 2);
    }
    else{
        content = content.substring(0,length - 1);
    }
    calc.display.value = content;
}
