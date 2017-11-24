function analyze() {
    var calc_input = $("input[name=display]").val();
    var dict_labels = [];
    $("input[name=dictionary]").each(function(){ dict_labels.push(this.value); });
    var check_boxes_status = [];
    $('input[type=checkbox]').each(function () {
        var status = (this.checked ? true : false);
        check_boxes_status.push(status);
    });
    var toggle_all_value = check_boxes_status[0];
    var active_dicts = check_boxes_status;
    active_dicts.shift();
    active_dicts.pop();
    active_dicts.pop();
    var data = JSON.stringify({"calc_input": calc_input, "active_dicts": active_dicts, "dict_labels": dict_labels, "toggle_all_value": toggle_all_value});
    $.ajax({
        url: "/contentanalysis",
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8'
    }).done(function (response) {
        response = JSON.parse(response);
        var error = response['error'];
        if(error != false){
            $('#status-analyze').css({ 'visibility': 'hidden' });
            $('#error-modal-message').html(error);
            $('#error-modal').modal();
        }
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        update_dictionary_buttons(dict_labels,active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
        update_check_all_checkbox(response['toggle_all_value']);
        $('#table').html(response['result_table']);
        $('.dataframe').DataTable( {
            "scrollX": true,
            'language': {
                'lengthMenu': 'Display _MENU_ documents',
                'info': 'Showing _START_ to _END_ of _TOTAL_ documents'
            },
            'lengthMenu': [[10, 25, 50, -1], [10, 25, 50, 'All']],
            'dom': "<'row'<'col-sm-2'l><'col-sm-3 pull-right'B>>" +
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
        });
    });
 }
function upload_dictionaries() {
    var formData = new FormData($('form')[0]);
    $.ajax({
        url: '/uploaddictionaries',
        type: 'POST',
        processData: false, // important
        contentType: false, // important
        data: formData
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        var toggle_all = response['toggle_all'];
        $('#display').val("");
        update_check_all_checkbox(toggle_all);
        update_dictionary_buttons(dict_labels,active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
    })
}
function toggle_checkbox(i) {
    var data = "";
    var dict_labels = [];
    $("input[name=dictionary]").each(function(){ dict_labels.push(this.value); });
    var check_boxes_status = [];
    $('input[type=checkbox]').each(function () {
        var status = (this.checked ? true : false);
        check_boxes_status.push(status);
    });
    var toggle_all_value = check_boxes_status[0];
    var active_dicts = check_boxes_status;
    active_dicts.shift();
    active_dicts.pop();
    active_dicts.pop();
    if(i == -1){
        data = JSON.stringify({"toggle_all": true, "dict_labels": dict_labels,
        "toggle_all_value": toggle_all_value});
    } else {
        var dict_label = dict_labels[i];
        data = JSON.stringify({"dict_label": dict_label, "toggle_all": false,
        "dict_labels": dict_labels, "active_dicts": active_dicts});
    }
    $.ajax({
        url: "/toggledictionary",
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8'
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        var toggle_all_value = response['toggle_all_value'];
        $('#display').val("");
        update_check_all_checkbox(toggle_all_value);
        update_dictionary_buttons(dict_labels,active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
    })
}
function delete_dictionary(i) {
    var dict_labels = [];
    $("input[name=dictionary]").each(function(){ dict_labels.push(this.value); });
    var dict_label = dict_labels[i];
    var active_dicts = $('input[id=dict_checkbox]:checked');
    var data = JSON.stringify({"dict_label": dict_label, "dict_labels": dict_labels, "active_dicts": active_dicts});
    $.ajax({
        url: "/deletedictionary",
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8'
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        $('#display').val("");
        if(dict_labels.length == 0){
            $('#forAllCheckBox').empty();
        }
        update_dictionary_buttons(dict_labels, active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
    })
}
function backspace(calc){
    var content = calc.display.value;
    var length = content.length;
    if(content[length -1] == "]"){
        content = content.substring(0,content.lastIndexOf("["));
    }else if(content.endsWith("sin(") || content.endsWith("cos(") ||
            content.endsWith("tan(") || content.endsWith("log(")){
        content = content.substring(0,length - 4);
    }else if(content.endsWith("^(") || content.endsWith("√(") ){
        content = content.substring(0,length - 2);
    }else{
        content = content.substring(0,length - 1);
    }
    calc.display.value = content;
}
function update_dictionary_buttons(dict_labels, active_dicts) {
    $('#dictionaryButtons').empty();
    for (var i = 0; i < dict_labels.length; i++) {
        if(active_dicts[i]) {
            var button = "<input type='button' value='" + dict_labels[i] + "'" +
                " onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";
            $('#dictionaryButtons').append(button);
        }
    }
}
function update_dictionary_checkboxes(dict_labels, active_dicts) {
    $('#checkboxes').empty();
    for (var i = 0; i < dict_labels.length; i++) {
        var checkbox = "<div class='forAllCheckBox' align='left'>" +
            "<input type='hidden' name='dictionary' value='"+dict_labels[i]+"'>" +
            "<label class='icon-checkbox";
        if(active_dicts[i]){
            checkbox += " checked";
        }
        checkbox += "'><input type='checkbox' id='dict_checkbox' onclick='toggle_checkbox("+i+")'";
        if(active_dicts[i]){
            checkbox += " checked";
        }
        checkbox += ">"+dict_labels[i]+ "</label>";
        checkbox += "<a role='button'><span class='glyphicon glyphicon-remove delete' onclick='delete_dictionary(" + i + ")'></span></a>";
        $('#checkboxes').append(checkbox);
    }
}
function update_check_all_checkbox(toggle_all_value) {
    $('#forAllCheckBox').empty();
    var check_all = "<label class='icon-checkbox";
    if(toggle_all_value) {
        check_all += " checked";
    }
    check_all += "'><input type='checkbox' id='allCheckBoxSelector' onclick='toggle_checkbox(-1)'";
    if(toggle_all_value) {
        check_all += " checked";
    }
    check_all += ">Check/Uncheck All</label>";
    $('#forAllCheckBox').append(check_all);
}
