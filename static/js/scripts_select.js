$(function() {

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

	$(".filepreview").hover(function(){ // when hovering
		if ($(this).children(".select-preview-filename").text().indexOf('...') >= 0) {

			$(this).children(".select-preview-filename-full").stop().animate({
				opacity: 1,
				top: 25
			}, 200);
		}
	}, 
							function(){ // when not hovering

		$(".select-preview-filename-full").stop().animate({
			opacity: 0,
			top: 0
		}, 200);
	});

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

	$.fn.hasLabel = function() {
		if (this.has('.classlabelbadge')) {
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
					// var badge =   "<div class='classlabelbadge'>"+ classLabelToApply +"</div>"
					
					$('.enabled').each(function(){
						if ($(this).hasLabel()) {
							$(this).children(".select-preview-label").html("");
						}
						$(".select-preview-label").html(classLabelToApply);
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

		$.ajax({
			type: "POST",
			url: document.URL,
			data: "",
			beforeSend: function(xhr){
				xhr.setRequestHeader("delete", "");
			},
			success: function(){
				enabled.remove();
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(errorThrown);
			}
		});
	});
});