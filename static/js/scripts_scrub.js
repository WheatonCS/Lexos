$(function() {

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

	$("#punctbox").click( function() {
		var timeToToggle = 100;
		if ($(this).children('input').is(':checked')) {
			$("#aposhyph").fadeIn(timeToToggle);
		}
		else {
			$("#aposhyph").fadeOut(timeToToggle);
		}
	});

	$('#xml-modal').on('show.bs.modal', function (e) {
        $.ajax({
            type: "POST",
            url: "/getAllTags",
            contentType: 'json',
            beforeSend: function(){
                // Do something
            },
            success: function(response) {
                j = JSON.parse(response);
                $.each(j, function(index, value) {
    				s = "<tr><td>"+value+"</td><td>Remove Tag Only|Remove Element and All Its Contents|Replace Element's Contents with Attribute Value</td></tr>";
    				$("#tagTable tbody").append(s);
				});
            	$("#xmlModalStatus").hide();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log("Error: " + errorThrown);
            }
		});
	});

	$('#xml-modal').on('hidden.bs.modal', function () {
        $("#xmlModalStatus").show();
        $("#tagTable tbody").empty();
	});

});

function downloadScrubbing() {
	// Unfortunately, you can't trigger a download with an ajax request; calling a
	// Flask route seems to be the easiest method.
	window.location = '/downloadScrubbing';
}

function doScrubbing(action) {
	$('#formAction').val(action);
	var formData = new FormData($('form')[0]);

	$.ajax({
	  url: '/doScrubbing',
	  type: 'POST',
	  processData: false, // important
	  contentType: false, // important
	  data: formData,
	  error: function (jqXHR, textStatus, errorThrown) {
	  	$("#error-modal .modal-body").html("Lexos could not apply the scrubbing actions.");
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