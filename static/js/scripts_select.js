$(function() {

	$.fn.center = function() {
	    
	    this.css("top", Math.max(0, ((($(window).height()) - $(this).outerHeight())/1.25) + 
	                                                $(window).scrollTop()) - 300 + "px");
	    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth())/4) + 
	                                                $(window).scrollLeft()) + "px");
	    return this;
	}

	// compresses filename and appends '...' to end
	var filePreviewTitleLimit = 10;

	$(".filepreview").each(function(){
		if ($(this).children(".select-preview-filename").text().length > filePreviewTitleLimit) {
			var newTitle = $(this).children(".select-preview-filename").text();
			newTitle = newTitle.slice(0, filePreviewTitleLimit-3);
			newTitle = newTitle + '... :';
			$(this).children(".select-preview-filename").html(newTitle);
		};
	});

	// animate full title of file if the title is compressed
	$(".filepreview").hover(function(){ // when hovering
		if ($(this).children(".select-preview-filename").text().indexOf('...') >= 0) {

			$(this).children(".select-preview-filename-full").stop().animate({
				opacity: 1,
				top: 30
			}, 200);
		}
	}, 
							function(){ // when not hovering

		$(".select-preview-filename-full").stop().animate({
			opacity: 0,
			top: 0
		}, 200);
	});

	// if ($('.select-preview-label').text().length == 0) {
	// 	$(".select-preview-label").hide();
	// }

	// add substring recommendation list/feature here

	$("#setenabling").change(function(e) {
		var setToEnable = $(this).val();

		$.ajax({
			type: 'POST',
			data: setToEnable,
			url: document.URL,
			beforeSend: function(xhr) {
				xhr.setRequestHeader('getSubchunks', '');
			},
			success: function(stringResp){
				var list = stringResp.split(',');
				var result = list.pop();

				var numEnabled = 0;
				var numTotal = list.length;
				for (var index in list) {
					var divID = '#' + list[index].replace(/^ /, '')
										.replace(/ $/, '')
										.replace(/\./g, '\\.');
					if (result == 'enable') {
						$(divID).addClass('enabled');
					}
					else {
						$(divID).removeClass('enabled');
					}
				}

				$(this).val('dummy');
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	$("#disableall").click(function() {

		$.ajax({
			type: "POST",
			url: document.URL,
			data: $(this).prop('id'),
			beforeSend: function(xhr){
				xhr.setRequestHeader('disableAll', '');
			},
			success: function(){
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
			success: function(){
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

	$(".filepreview").click(function() {
		var id = $(this).prop('id');
		var that = $(this);

		// toggles active class on select page
		$.ajax({
			type: 'POST',
			url: document.URL,
			data: id.toString(),
			contentType: 'charset=UTF-8',
			success: function(){
				that.toggleClass('enabled');
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	// new jQuery function to check and see if element has
	// the DOM element '.classlabelbadge'
	$.fn.hasLabel = function() {
		if (this.children(".select-preview-label").text().length > 0) {
			return true;
		} else {
			return false;
		}
	}

	// ajax call to send tag metadata on click
	$("#tagsubmit").click(function(){
		if ($("#tagfield").val()){
			// lowercases the tag. Can change to upper or whichever
			var classLabelToApply = $("#tagfield").val();

			// ajax call to send tag to backend
			$.ajax({
				type: 'POST',
				url: document.URL,
				data: classLabelToApply,
				contentType: 'charset=UTF-8',
				beforeSend: function(xhr){
					xhr.setRequestHeader('applyClassLabel', '');
				},
				success: function(){
					// have visual feedback showing tag was applied
					
					$('.enabled').each(function(){
						if ($(this).hasLabel()) {
							console.log("has label");
							$(this).children(".select-preview-label").html("");
						}
						$(this).children(".select-preview-label").html(classLabelToApply);
					});
				},
				error: function(jqXHR, textStatus, errorThrown){
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		}
	});

	$("#delete").click(function(){

		var enabled = $(".enabled");

		// if there are selected files
		if (enabled.length > 0) {

			// center the caution prompt in the window
			$('#delete-confirm-wrapper').center();

			var confirmationPrompt = $('#delete-confirm-wrapper');
			
			// show the prompt
			confirmationPrompt.show();
			confirmationPrompt.addClass("showing");
			
			// if they click cancel button, do nothing (just disappear)
			$('#cancel-bttn').click(function(){
				confirmationPrompt.removeClass("showing");
			})

			// if click confirm, delete the selection
			$('#confirm-delete-bttn').click(function() {

				$.ajax({
					type: "POST",
					url: document.URL,
					data: "",
					beforeSend: function(xhr){
						xhr.setRequestHeader("delete", "");
					},
					success: function(){

						confirmationPrompt.removeClass("showing");
						confirmationPrompt.hide();

						enabled.remove();

					},
					error: function(jqXHR, textStatus, errorThrown){
						console.log(errorThrown);
					}
				});
			});
		}
	});
});