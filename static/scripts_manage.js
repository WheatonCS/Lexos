$(function() {
	$("#setenabling").change(function(e) {
		var setToEnable = $(this).val();

		var xhr = new XMLHttpRequest();

		xhr.open("POST", document.URL, false);
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
								.replace(/\./g, '\\.');
			if (result == 'enable') {
				$(divID).addClass('enabled');
			}
			else {
				$(divID).removeClass('enabled');
			}
		}

		$(this).val('dummy');

		if ($(".filepreview.enabled").length == 0) {
			document.cookie = 'nofiles';
		}
	});

	$("#disableall").click(function() {
		var xhr = new XMLHttpRequest();

		xhr.open("POST", document.URL, false);
		xhr.setRequestHeader('disableAll', '');
		xhr.send();

		$(".filepreview").each(function() {
			$(this).removeClass("enabled");
		});

		document.cookie = 'nofiles';
	});

	$(".filepreview").click(function() {
		var id = $(this).prop('id');
		var xhr = new XMLHttpRequest();
		xhr.open("POST", document.URL, false);
		xhr.send($(this).prop('id'));

		$(this).toggleClass('enabled');

		if ($(".filepreview.enabled").length == 0) {
			document.cookie = 'nofiles';
		}
		else {
			document.cookie = 'files';
		}
	});
});