$(function() {

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

		// var xhr = new XMLHttpRequest();

		// xhr.open("POST", document.URL, false);
		// xhr.setRequestHeader('getSubchunks', '');
		// xhr.send(setToEnable);

		// var stringResp = xhr.responseText;
		// var list = stringResp.split(',');
		// var result = list.pop();

		// var numEnabled = 0;
		// var numTotal = list.length;
		// for (var index in list) {
		// 	var divID = '#' + list[index].replace(/^ /, '')
		// 						.replace(/ $/, '')
		// 						.replace(/\./g, '\\.');
		// 	if (result == 'enable') {
		// 		$(divID).addClass('enabled');
		// 	}
		// 	else {
		// 		$(divID).removeClass('enabled');
		// 	}
		// }

		// $(this).val('dummy');
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

		// $(".filepreview").each(function() {
		// 	$(this).removeClass("enabled");
		// });
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

			// $(".filepreview").each(function() {
			// 	$(this).removeClass("enabled");
			// });
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

		// var xhr = new XMLHttpRequest();
		// xhr.open("POST", document.URL, false);
		// xhr.send($(this).prop('id'));

		// $(this).toggleClass('enabled');	
	});

	// ajax call to send tag metadata on click
	$("#tagsubmit").click(function(){
		if ($(".tagfield").val()){
			// lowercases the tag. Can change to upper or whichever
			var tagToApply = $(".tagfield").val().toLowerCase();

			// ajax call to send tag to backend
			$.ajax({
				type: 'POST',
				url: document.URL,
				data: tagToApply,
				contentType: 'charset=UTF-8',
				beforeSend: function(xhr){
					xhr.setRequestHeader('applyTag', '');
				},
				success: function(){
					// have visual feedback showing tag was applied
					// console.log("tag applied");
					var badge = "<div class='tagbadge'>"+ tagToApply +"</div>"
					$('.enabled').each(function(){
						$(this).append(badge);
					});
				},
				error: function(jqXHR, textStatus, errorThrown){
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});

			// var xhr = new XMLHttpRequest();
			// xhr.open("POST", document.URL, false);
			// xhr.send(tagToApply);
		}
	});

	$("#delete").click(function(){

		var enabled = $(".enabled");
		var enabledDivs = [];

		enabled.each(function(index, value){
			enabledDivs.push($(value).attr('id'));
		});

		console.log(enabledDivs);

		$.ajax({
			type: "POST",
			url: document.URL,
			data: enabledDivs,
			beforeSend: function(xhr){
				xhr.setRequestHeader("delete", "");
			},
			success: function(){
				console.log("success");
				//re-render screen
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(errorThrown);
			}
		});
	});
});