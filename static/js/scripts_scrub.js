$(function() {
	if ($("input[name='haveGutenberg']")) {
		$('#gutenberg-modal').modal();
	}
	$("#actions").addClass("actions-scrub");

	$(".has-chevron").on("click", function() {
		$(this).find("span").toggleClass("down");
		$(this).next().collapse('toggle');
	});

	// display additional options on load
	var advancedOptions = $("#advanced-title");
	advancedOptions.find('.icon-arrow-right').addClass("showing");
	advancedOptions.siblings('.expansion').slideToggle(0);

	$('#swfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 25) {filename = filename.substring(0, 24) + "...";}
		$("#swfileselectbttnlabel").html(filename);
	});

	$('#lemfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 25) {filename = filename.substring(0, 24) + "...";}
		$("#lemfileselectbttnlabel").html(filename);
	});

	$('#consfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 25) {filename = filename.substring(0, 24) + "...";}
		$("#consfileselectbttnlabel").html(filename);
	});

	$('#scfileselect').change(function(ev) {
		filename = ev.target.files[0].name;
		if (filename.length > 25) {filename = filename.substring(0, 24) + "...";}
		$("#scfileselectbttnlabel").html(filename);
	});


	$(".bttnfilelabels").click( function() {
		//swfileselect, lemfileselect, consfileselect, scfileselect
		var filetype = $(this).attr('id').replace('bttnlabel', '');
		usingCache = $('#usecache'+filetype).attr('disabled') != 'disabled';

		if ((usingCache) || ($(this).attr('id') != '')) {
			//$(this).siblings('.scrub-upload').attr('value', '');
			// Next two lines clear the file input; it's hard to find a cross-browser solution			
			$("#"+filetype).val('');
			$("#"+filetype).replaceWith($("#"+filetype).clone(true));
			$("#usecache"+filetype).attr('disabled', 'disabled');
			$(this).text('');
		}

		// Do Ajax
        $.ajax({
            type: "POST",
            url: "/removeUploadLabels",
            data: $(this).text().toString(),
            contentType: 'text/plain',
            headers: { 'option': filetype+'[]' },
            beforeSend: function(){
                //alert('Sending...');
            },
            success: function(response) {
                //console.log(response);
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log("Error: " + errorThrown);
            }
		});
	});

	$("#whitespacebox").click( function() {
		var timeToToggle = 100;
		if ($(this).is(':checked')) {
			$("#whitespace").removeClass("hidden");
			//$("#whitespace").fadeIn(timeToToggle);
		}
		else {
			$("#whitespace").addClass("hidden");
			//$("#whitespace").fadeOut(timeToToggle);
		}
	});
	$("#entityrules").change(function(){
		console.log($("#entityrules")[0].value);
		if($("#entityrules")[0].value == "MUFI-3" || $("#entityrules")[0].value == "MUFI-4") {
			document.getElementById("MUFI-warning").style.display = "inline-block";
			}
		else 
		{
			document.getElementById("MUFI-warning").style.display = "none";
		}
		});

	$("#tagbox").click( function() {
		var timeToToggle = 100;
		if ($(this).is(':checked')) {
			$("#tag").removeClass("hidden");
			//$("#whitespace").fadeIn(timeToToggle);
		}
		else {
			$("#tag").addClass("hidden");
			//$("#whitespace").fadeOut(timeToToggle);
		}
	});


	$("#set-tags-button").click( function() {
	    if ( $( "#allTags" ) ) {
            var allTags =($( "#allTags")[0].value);
            allTags = JSON.stringify(allTags);
            $.ajax({
                type: "POST",
                url: "/setAllTagsTable",
                data: allTags,
                "contentType": 'application/json; charset=utf-8',
                "dataType": "json",
                beforeSend: function(){
                $('<p/>', {
					    id: 'xmlModalStatus',
					    style: 'width:100px;margin:50px auto;z-index:1000;',
					}).appendTo('#xmlModalBody');
				$("#xmlModalStatus").append('<img src="/static/images/loading_icon.svg?ver=2.5" alt="Loading..."/>');
                },
                success: function(response) {
                    $("#tagTable").empty().remove();
				    var t = '<table id="tagTable" class="table table-condensed table-striped table-bordered"></table>';
			    	$('#xmlModalBody').append(t);
			    	$("#tagTable").append('<thead><tr><th>Element</th><th colspan="2">Action</th></tr></thead>');
                 	$("#tagTable").append('<tbody></tbody>');
		    		$("#tagTable tbody").append(response);

                 	$("#xmlModalStatus").remove();
	    			var value=$("#myselect option:selected").val();
	    			var text=$("#myselect option:selected").text();
                    },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log("Error: " + errorThrown);
                    }
		        });
        }
    });

	$("#punctbox").mousedown( function() {
		var timeToToggle = 300;

		if ($('#aposhyph')[0].style.cssText=="display: none;") {
			$("#aposhyph").fadeIn(timeToToggle);
		}
		else {
			$("#aposhyph").fadeOut(timeToToggle);
			$('#aposhyph')[0].style.cssText=="display: none;"
		}
	});

	$('#xml-modal').on('show.bs.modal', function (e) {
        $.ajax({
            type: "POST",
            url: "/getTagsTable",
            contentType: 'json',
            beforeSend: function(){
                $('<p/>', {
					    id: 'xmlModalStatus',
					    style: 'width:100px;margin:50px auto;z-index:1000;',
					}).appendTo('#xmlModalBody');

				$("#xmlModalStatus").append('<img src="/static/images/loading_icon.svg?ver=2.5" alt="Loading..."/>');
            },
            success: function(response) {
                j = JSON.parse(response);
				var t = '<table id="tagTable" class="table table-condensed table-striped table-bordered"></table>';
				$('#xmlModalBody').append(t);
				$("#tagTable").append('<thead><tr><th>Element</th><th colspan="2">Action</th></tr></thead>');
            	$("#tagTable").append('<tbody></tbody>');
				$("#tagTable tbody").append(j);
				
            	$("#xmlModalStatus").remove();
				var value=$("#myselect option:selected").val();
				var text=$("#myselect option:selected").text();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log("Error: " + errorThrown);
            }
		});
	});

	$('#xml-modal').on('hidden.bs.modal', function () {
        $("#tagTable").empty().remove();
	});

});

function downloadScrubbing() {
	// Unfortunately, you can't trigger a download with an ajax request; calling a
	// Flask route seems to be the easiest method.
	window.location = '/downloadScrubbing';
}

function doScrubbing(action) {
	if ( $('#num_active_files').val() == "0" ) {
		$('#error-modal').modal();
		return;
	}

	$('#formAction').val(action);
	var formData = new FormData($('form')[0]);

	$.ajax({
	  url: '/doScrubbing',
	  type: 'POST',
	  processData: false, // important
	  contentType: false, // important
	  data: formData,
	  error: function (jqXHR, textStatus, errorThrown) {
	  	$("#error-modal-message").html("Lexos could not apply the scrubbing actions.");
		$("#error-modal").modal();
		console.log("bad: " + textStatus + ": " + errorThrown);
	  }
	}).done(function(response) {
		response = JSON.parse(response);
		$("#preview-body").empty();
		$.each(response["data"], function(i, item) {
		    fileID = $(this)[0];
		    filename = $(this)[1];
		    fileLabel = $(this)[2];
		    fileContents = $(this)[3];
			fieldset = $("<fieldset></fieldset>");
			fieldset.append('<legend class="has-tooltip" style="color:#999; width:auto;">'+filename+'</legend>');
			fieldset.append('<div class="filecontents">'+fileContents+'</div>'); //Keep this with no whitespace!
			$("#preview-body").append(fieldset);
		});		
	});
}
