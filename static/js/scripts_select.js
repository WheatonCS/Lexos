$(function() {
	$(".select-preview-text").click(function() {
		var id = $(this).parent('.select-preview-wrapper').prop('id');
		var that = $(this);

		// toggles active class on select page
		$.ajax({
			type: "POST",
			url: document.URL,
			data: id.toString(),
			contentType: 'charset=UTF-8',
			beforeSend: function(xhr){
				xhr.setRequestHeader('toggleFile', '');
			},
			success: function() {
				that.parent('.select-preview-wrapper').toggleClass('enabled');
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	$(".select-preview-filename").each(function() {
		$(this).prop('contenteditable', 'true');
	});

	$('.select-preview-filename').keydown(function(event) {
		var keyCode = event.which;

		if (keyCode == 13) { // "Enter"
			var contents = $(this).text();
			var id = $(this).parent().prop('id');

			// toggles active class on select page
			$.ajax({
				type: "POST",
				url: document.URL,
				data: id.toString(),
				contentType: 'charset=UTF-8',
				beforeSend: function(xhr){
					xhr.setRequestHeader('setLabel', contents.toString());
				},
				success: function() {
					alert("Label for " + id.toString() + " set to " + contents.toString());
				},
				error: function(jqXHR, textStatus, errorThrown){
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});

			event.preventDefault();
		}
	});


	$("#disableall").click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: $(this).prop('id'),
			beforeSend: function(xhr){
				xhr.setRequestHeader('disableAll', '');
			},
			success: function() {
				$(".filepreview").each(function() {
					$(this).removeClass("enabled");
				});
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	$("#selectall").click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: $(this).prop('id'),
			beforeSend: function(xhr){
				xhr.setRequestHeader('selectAll', '');
			},
			success: function() {
				$(".filepreview").each(function() {
					$(this).addClass("enabled");
				});
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	// ajax call to send tag metadata on click
	$("#tagsubmit").click(function() {
		if ($("#tagfield").val()){
			// lowercases the tag. Can change to upper or whichever
			var classLabelToApply = $("#tagfield").val();

			// ajax call to send tag to backend
			$.ajax({
				type: "POST",
				url: document.URL,
				data: classLabelToApply,
				contentType: 'charset=UTF-8',
				beforeSend: function(xhr){
					xhr.setRequestHeader('applyClassLabel', '');
				},
				success: function() {
					// have visual feedback showing tag was applied
					$('.enabled').each(function() {
						$(this).children(".select-preview-label").html(classLabelToApply);
					});
				},
				error: function(jqXHR, textStatus, errorThrown){
					// display error if one exists
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		}
	});

	// center the caution prompt in the window
	$('#delete-confirm-wrapper').center();

	$("#delete").click(function() {
		var enabled = $(".enabled");

		// if there are selected files
		if (enabled.length > 0) {
			// show the prompt
			$('#delete-confirm-wrapper').addClass("showing");
		}
	});
			
	// if they click cancel button, do nothing (just disappear)
	$('#cancel-bttn').click(function() {
		$('#delete-confirm-wrapper').removeClass("showing");
	});

	// if click confirm, delete the selection
	$('#confirm-delete-bttn').click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: "",
			beforeSend: function(xhr){
				xhr.setRequestHeader("deleteActive", "");
			},
			success: function() {
				$('#delete-confirm-wrapper').removeClass("showing");
				enabled.remove();
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(errorThrown);
			}
		});
	});
});