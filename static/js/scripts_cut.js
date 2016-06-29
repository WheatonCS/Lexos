// Function to convert the form data into a JSON object
function jsonifyForm() {
    var form = {};
    $.each($("form").serializeArray(), function (i, field) {
        form[field.name] = field.value || "";
    });
    return form;
}

function downloadCutting() {
    // Unfortunately, you can't trigger a download with an ajax request; calling a
    // Flask route seems to be the easiest method.
    window.location = '/downloadCutting';
}

function doCutting(action) {
    // Show the processing icon
    $("#status-prepare").css({"visibility":"visible"});
    var loadingTimer = setTimeout(function() {
        if($("#status-prepare").css('visibility') == "visible"){
            $('#error-modal-message').html("It seems to be taking a while to load. If you aren't processing a large number of documents, please reload the page and try again.");
            $('#error-modal').modal();
        }
    }, 10000);

    // Validate the form data -- save errors into errors array
    var errors = [];
    var err1 = 'You have no active documents. Please activate at least one document using the <a href=\"{{ url_for("manage") }}\">Manage</a> tool or <a href=\"{{ url_for("upload") }}\">upload</> a new document.';
    var err2 = "You must provide a string to cut on.";
    var err3 = "You must provide a default cutting value.";
    var err4 = "Default cutting: Invalid segment size.";
    var err5 = "Default cutting: Invalid overlap value.";
    var err6 = "Individual cutting: Invalid segment size.";
    var err7 = "Individual cutting: Invalid overlap value.";

    // Confirm that there are active files
    if ($('#num_active_files').val() == "0" ) {
        errors.push(err1);
    }

    // If cut by milestone is checked make sure there is a milestone value
    if ($("#cutByMS").is(":checked")){
        if ($("#MScutWord").val() == '') {
            errors.push(err2);
        }
    }
    else {
        // Make sure there is a default cutting value
        if ($("#overallcutvalue").val() == '') {
            errors.push(err3);
        }
        else {
            var overallcutvalue = parseInt($("#overallcutvalue").val());
            var overallOverlapValue = parseInt($("#overallOverlapValue").val());
            var individualOverlap = parseInt($("#individualOverlap").val());
            var individualCutValue = $("#individualCutValue").val();

            // Make sure the overall segment size is valid      
            if((Math.abs(Math.round(overallcutvalue)) != overallcutvalue) || overallcutvalue == 0) {
                errors.push(err4);
            }
            // Make sure the overall overlap is valid       
            if ((overallcutvalue <= overallOverlapValue) || (Math.abs(Math.round(overallOverlapValue)) != overallOverlapValue)) {
                errors.push(err5);
            }

            // If there are individual segment cuts
            if (individualCutValue != '') {
                individualCutValue = parseInt(individualCutValue);
                // Make sure the individual segment size is valid       
                if ((Math.abs(Math.round(individualCutValue)) != individualCutValue)) {
                    errors.push(err6);
                }
                // Make sure the individual overlap is valid        
                if ((individualCutValue <= individualOverlap) || (Math.abs(Math.round(individualOverlap)) != individualOverlap)) {
                    errors.push(err7);
                }
            }
        } 
    }

    // Check for warnings
    var warnings = false;
    var maxSegs = 100;
    var defCutTypeValue= $("input[name='cutType']:checked").val();
    var cutVal = parseInt($("input[name='cutValue']").val());
    var overVal = parseInt($("#overallOverlapValue").val());
    var needsWarning = false;
    var indivdivs = $(".cuttingoptionswrapper.ind");
    var eltswithoutindividualopts = new Array();

    indivdivs.each(function() {     
        var thisCutVal = $("#individualCutValue",this).val();
        var thisOverVal = $("#individualOverlap",this).val();
        if (thisCutVal!= '') {
            thisCutVal=parseInt(thisCutVal);
            thisOverVal = parseInt(thisOverVal);
        }
        var listindex = indivdivs.index(this);
        currID = activeFileIDs[listindex];
        var isCutByMS = $(".indivMS",this).is(":checked");
        if (!isCutByMS && thisCutVal == '') {
            eltswithoutindividualopts.push(listindex);
        }
        if (thisCutVal!='') {
            var thisCutType = $("input[name='cutType_" + currID + "']:checked").val();
            if (!(isCutByMS)) {
                if (thisCutType == "letters" && (numChar[listindex]-thisOverVal)/(thisCutVal-thisOverVal) > maxSegs){
                    needsWarning = true;
                } else if (thisCutType == "words" && (numWord[listindex]-thisOverVal)/(thisCutVal-thisOverVal) > maxSegs){
                    needsWarning = true;
                } else if (thisCutType == "lines" && (numLine[listindex]-thisOverVal)/(thisCutVal-thisOverVal) > maxSegs){
                    needsWarning = true;
                } else if (thisCutVal > maxSegs){
                    needsWarning = true;
                }
            }
        }//;    
    });
    
    if ($("input[name='cutByMS']:checked").length == 0) {
        if (defCutTypeValue == "letters") {
            eltswithoutindividualopts.forEach(function(elt) {
                if ((numChar[elt]-cutVal)/(cutVal-overVal) > maxSegs) {
                    needsWarning = true;
                }
            });
        } else if (defCutTypeValue == "words") {
            eltswithoutindividualopts.forEach(function(elt) {
                if ((numWord[elt]-cutVal)/(cutVal-overVal) > maxSegs) {
                    needsWarning = true;
                }
            });
        } else if (defCutTypeValue == "lines") {
            eltswithoutindividualopts.forEach(function(elt) {
                if ((numLine[elt]-cutVal)/(cutVal-overVal) > maxSegs){
                    needsWarning = true;
                }
            });
        } else if (cutVal > maxSegs && eltswithoutindividualopts.length > 0) {
            needsWarning = true;
        }
    }

    // If there are no errors or warnings make the Ajax request
    if (errors.length == 0) {
        /* It's not really efficient to create a FormData and a json object,
           but the former is easier to pass to lexos.py functions, and the
           latter is easier for the ajax response to use. */
        var formData = new FormData($('form')[0]);
        formData.append("action", action);
        var jsonform =  jsonifyForm();
        $.extend(jsonform, {"action": action});
        $.ajax({
          url: '/doCutting',
          type: 'POST',
          processData: false, // important
          contentType: false, // important
          beforeSend: function() {
		    if (needsWarning) {
		        warnings = true;
		        $('#confirm-modal-message').html("Current cut settings will result in over 100 new segments.  Please be patient if you continue.");
		        $('#confirm-modal').modal({
		            backdrop: 'static',
		            keyboard: false
		        })
		        .one('click', '#continue', function() {
		            warnings = false;
		        });
		    }
		    if (warnings == true) { return false; }
          },
          data: formData,
          error: function (jqXHR, textStatus, errorThrown) {
            $("#error-modal-message").html("Lexos could not apply the cutting actions.");
            $("#error-modal").modal();
            console.log("bad: " + textStatus + ": " + errorThrown);
          }
        }).done(function(response) {
            clearTimeout(loadingTimer);
            response = JSON.parse(response);
            $("#preview-body").empty(); // Correct
            $.each(response["data"], function(i, item) {
                fileID = $(this)[0];
                filename = $(this)[1];
                fileLabel = $(this)[2];
                fileContents = $(this)[3];
                var indivcutbuttons = '<a id="indivcutbuttons_'+fileID+'" onclick="toggleIndivCutOptions('+fileID+');" class="bttn indivcutbuttons" role="button">Individual Options</a></legend>';
                fieldset = $('<fieldset class="individualpreviewwrapper"><legend class="individualpreviewlegend has-tooltip" style="color:#999; width:auto;">'+filename+' '+indivcutbuttons+'</fieldset>');
                var indcutoptswrap = '<div id="indcutoptswrap_'+fileID+'" class="cuttingoptionswrapper ind hidden"><fieldset class="cuttingoptionsfieldset"><legend class="individualcuttingoptionstitle">Individual Cutting Options</legend><div class="cuttingdiv individcut"><div class="row"><div class="col-md-5"><label class="radio sizeradio"><input type="radio" name="cutType_'+fileID+'" id="cutTypeIndLetters_'+fileID+'" value="letters"/>Characters/Segment</label></div><div class="col-md-7"><label class="radio sizeradio"><input type="radio" name="cutType_'+fileID+'" id="cutTypeIndWords_'+fileID+'" value="words"/>Tokens/Segment</label></div></div><div class="row cutting-radio"><div class="col-md-5"><label class="radio sizeradio"><input type="radio" name="cutType_'+fileID+'" id="cutTypeIndLines_'+fileID+'" value="lines"/>Lines/Segment</label></div><div class="col-md-7"><label class="radio numberradio"><input type="radio" name="cutType_'+fileID+'" id="cutTypeIndNumber_'+fileID+'" value="number"/>Segments/Document</label></div></div></div><div class="row"><div class="col-md-6 pull-right" style="padding-left:2px;padding-right:5%;"><label><span id="numOf'+fileID+'" class="cut-label-text">Number of Segments:</span><input type="number" min="0" name="cutValue_'+fileID+'" class="cut-text-input" id="individualCutValue" value=""/></label></div></div><div class="row overlap-div"><div class="col-md-6 pull-right" style="padding-left:2px;padding-right:5%;"><label>Overlap: <input type="number" min="0" name="cutOverlap_'+fileID+'" class="cut-text-input overlap-input" id="individualOverlap" value=""/></label></div></div><div id="lastprop-div_'+fileID+'" class="row lastprop-div"><div class="col-md-6 pull-right" style="padding-left:2px;padding-right:1%;"><label>Last Proportion Threshold: <input type="number" min="0" id="cutLastProp_'+fileID+'" name="cutLastProp_'+fileID+'" class="cut-text-input lastprop-input" value="50"/> %</label></div></div><div class="row"><div class="col-md-6 pull-right" style="padding-left:2px;padding-right:5%;"><label>Cutset Label: <input type="text" name="cutsetnaming_'+fileID+'" class="cutsetnaming" value="'+filename+'"></label></div></div><div class="row cuttingdiv" id="cutByMSdiv"><div class="col-md-4"><label><input type="checkbox" class="indivMS" name="cutByMS_'+fileID+'" id="cutByMS_'+fileID+'"/>Cut by Milestone</label></div><div class="col-md-8 pull-right" id="MSoptspan" style="display:none;"><span>Cut document on this term <input type="text" class="indivMSinput" name="MScutWord_'+fileID+'" id="MScutWord'+fileID+'" value=""/></span></div></div></fieldset></div>';
                fieldset.append(indcutoptswrap);
                if ($.type(fileContents) === "string") {
                    fieldset.append('<div class="filecontents">'+fileContents+'</div>'); //Keep this with no whitespace!
                }
                else {
                    $.each(fileContents, function(i, segment) {
                        segmentLabel = segment[0];
                        segmentString = segment[1];
                        fieldset.append('<div class="filechunk"><span class="filechunklabel">'+segmentLabel+'</span><div>'+segmentString+'</div></div>');
                    });
                }
                $("#preview-body").append(fieldset);
                // Hide the individual cutting wrapper if the form doesn't contain values for it
                if (!('cutType_'+fileID in formData) && formData['cutType_'+fileID] != '') {
                    $('#indcutoptswrap_'+fileID).addClass("hidden");
                }
                // Check the cut type boxes
                if (formData['cutTypeInd'] == 'letters') {
                    $('#cutTypeIndLetters_'+fileID).prop('checked', true);
                }
                if (formData['cutTypeInd'] == 'words') {
                    $('#cutTypeIndWords_'+fileID).prop('checked', true);
                }
                if (formData['cutTypeInd'] == 'lines') {
                    $('#cutTypeIndLines_'+fileID).prop('checked', true);
                }
                if (formData['cutTypeInd'] == 'number') {
                    $('#cutTypeIndNumber_'+fileID).prop('checked', true);
                    $('#numOf_'+fileID).html("Number of Segments");
                    $('#lastprop-div').addClass('transparent');
                    $('#cutLastProp_'+fileID).prop('disabled', true);
                }
                if (formData['Overlap']) {
                    $('#cutOverlap_'+fileID).val(formData['Overlap']);
                }
                else {
                    $('#cutOverlap_'+fileID).val(0);                    
                }
                if (formData['cutLastProp_'+fileID]) {
                    $('#lastprop-div_'+fileID).val(formData['#cutLastProp_'+fileID]);
                }
                if (formData['cutType'] == 'milestone') {
                    $('#cutTypeIndNumber_'+fileID).prop('checked', true);
                }
                if (formData['MScutWord_'+fileID] == 'milestone') {
                    $('#MScutWord'+fileID).val(formData['cuttingoptions']['cutValue']);
                }
            });
            if (action == "apply") {
                $("#downloadCutting").removeClass("hidden");
            }                   
            $("#status-prepare").css({"visibility":"hidden"});                  
        });
    }
    else {
        $("#status-prepare").css({"visibility":"hidden"});
        $('#error-modal-message').html(errors[0]);
        $('#error-modal').modal();        
    }
}

$(function() {

    $("#actions").addClass("actions-cut");
    
    // Toggle cutting options when radio buttons with different classes are clicked
    var timeToToggle = 150;
    $(".sizeradio").click( function() {
        var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
        cuttingValueLabel.text("Segment Size:");

        $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
                .animate({ opacity: 1 }, timeToToggle)
                .find('.lastprop-input').prop('disabled', false);

        $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
                .animate({ opacity: 1 }, timeToToggle)
                .find('.overlap-input').prop('disabled', false);
    });

    $(".numberradio").click( function() {
        var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
        cuttingValueLabel.text("Number of Segments:");

        $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
                .animate({ opacity: 0.2 }, timeToToggle)
                .find('.lastprop-input').prop('disabled', true);

        $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
                .animate({ opacity: 0.2 }, timeToToggle)
                .find('.overlap-input').prop('disabled', true);
    });

    // Toggle individual cut options on load
    $(".indivcutbuttons").click( function() {
        var toggleDiv = $(this).closest('.individualpreviewwrapper').find('.cuttingoptionswrapper');
        toggleDiv.toggleClass("hidden");
        // slideToggle() only works if the div is first set to 'display:none'
        //toggleDiv.slideToggle(timeToToggle);
    });

    // Toggle milestone options
    function showMilestoneOptions(){
        if ($("#cutByMS").is(":checked")){
            $("#MSoptspan").show();
            $("#cuttingdiv").hide();
        } else {
            $("#MSoptspan").hide();
            $("#cuttingdiv").show();
        }
    }

    $("#cutByMS").click(showMilestoneOptions);

    showMilestoneOptions();

    $(".indivMS").click( function() {
        if ($(this).is(":checked")) {
            $(this).parents("#cutByMSdiv").filter(":first").children("#MSoptspan").show();
            $(this).parents("#cutByMSdiv").filter(":first")
            .parents(".cuttingoptionswrapper").find(".individcut").hide();
        } else {
            $(this).parents("#cutByMSdiv").filter(":first").children("#MSoptspan").hide();
            $(this).parents("#cutByMSdiv").filter(":first")
            .parents(".cuttingoptionswrapper").find(".individcut").show();
        }
    });

});