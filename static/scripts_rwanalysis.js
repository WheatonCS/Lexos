$(function() {
	$(".minifilepreview").click(function() {
		$(this).siblings(".minifilepreview").removeClass('enabled');
		$(this).addClass('enabled');
		$("#filetorollinganalyze").val($(this).prop('id'));
	});

	$("#radioratio").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeIn(timeToToggle);
		$(".rollingsearchwordoptdiv").css('display', 'inline');
	});
	$("#radioaverage").click(function() {
		var timeToToggle = 150;
		$(".rollingsearchwordoptdiv").fadeOut(timeToToggle);
	});

	$("#radioinputletter").click(function() {
		var oldVal = $(".rollinginput").val();
		$(".rollinginput").val(oldVal.slice(0,1));
	});

	$("#radioinputword").click(function() {
		if ($("#windowletter").prop('checked')) {
			$("#windowword").click();
		}
	});
	$("#radiowindowletter").click(function() {
		if ($("#inputword").prop('checked')) {
			$("#rwasubmiterrormessage3").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	$(".rollinginput").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
			if ($(this).val().length > 0 && $("#inputletter").prop('checked')) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});
	$("#rollingwindowsize").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
			key = String.fromCharCode( key );
			var regex = /[0-9]|\./;
			if( !regex.test(key) ) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});

	$("form").submit(function() {
		var empty = $("input").filter(function() {
			return this.value == '' && (this.type == 'text' || this.type == 'number');
		});
		numEmpty = empty.length;
		if ($(".minifilepreview.enabled").length == 0) {
			$("#rwasubmiterrormessage2").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if (numEmpty > 0 && !(numEmpty == 1 && empty[0].id == 'rollingsearchwordopt' && $("#rollingaverage").prop('checked')) ) {
			$("#rwasubmiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
	});

	// function makeRWAGraph() {
	// 	if ($('#rwagraphdiv').text() == 'True') {
	// 		var dataArray = [];
	// 		$.getJSON(document.URL+'_data', 0, function(data) {
	// 			dataArray = data.results;
	// 			alert(dataArray);
	// 		});

	// 		alert(dataArray);
	// 	}
	// 	else {
	// 		alert($('#rwagraphdiv').text());
	// 	}
	// }

	// makeRWAGraph();
});