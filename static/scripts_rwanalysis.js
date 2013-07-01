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

	$("form").submit(function() {
		if ($(".minifilepreview.enabled").length == 0) {
			$("#rwasubmiterrormessage2").show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			var empty = $("input").filter(function() {
				return this.value == '' && this.type == 'text';
			});
			numEmpty = empty.length;
			if (numEmpty > 0) {
				for (var index = 0; index < numEmpty; index++) {
					id = empty[index].id;
					if ( !(id == 'rollingsearchwordopt' && !$("#rollingratio").prop('checked')) ) {
						$("#rwasubmiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
						return false;
					}
				}
			}
		}
	});
});