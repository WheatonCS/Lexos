$(function() {
	// Ajax gives the XMLHttpRequest
	var ajaxRequestURL = document.getElementById("manage").action;
	
	$("#setenabling").change(function(e) {
		var setToEnable = $(this).val();

		var xhr = new XMLHttpRequest();
		xhr.open("POST", ajaxRequestURL, false);
		xhr.setRequestHeader('getSubchunks', '');
		xhr.send(setToEnable);

		var stringResp = xhr.responseText;
		var list = stringResp.split(',');
		var result = list.pop();

		var numEnabled = 0;
		var numTotal = list.length;
		for (var index in list) {
			var divID = '#' + list[index].replace(/^ /, '')
								.replace(/ $/, '')
								.replace(/\./, '\\.');
			if (result == 'enable') {
				$(divID).addClass('enabled');
			}
			else {
				$(divID).removeClass('enabled');
			}
		}

		$(this).val('dummy');
	});


	$("option").click(function() {
		alert("boom1");
	});

	$("#disableall").click(function() {
		var xhr = new XMLHttpRequest();

		xhr.open("POST", ajaxRequestURL, false);
		xhr.setRequestHeader('disableAll', '');
		xhr.send();

		$(".filepreview").each(function() {
			$(this).removeClass("enabled");
		});

	});

	$(".filepreview").click(function() {
		// var inputToToggle = $(this).children('.filestatus');
		// // alert(inputToToggle.prop('disabled'));
		// inputToToggle.prop('disabled', !inputToToggle.prop('disabled'));
		// $(this).toggleClass('enabled');
		var id = $(this).prop('id');
		var xhr = new XMLHttpRequest();
		xhr.open("POST", ajaxRequestURL, false);
		xhr.send($(this).prop('id'));

		$(this).toggleClass('enabled');
	});
});

function haveactivefiles() {
	var xhr = new XMLHttpRequest();

	xhr.open("POST", ajaxRequestURL, false);
	xhr.setRequestHeader('testforactive', '');
	xhr.send();

	if (xhr.responseText == 'False') {
		alert("You have no files enabled.");
		return false;
	}
}