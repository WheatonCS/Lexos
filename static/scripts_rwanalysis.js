$(function() {

	$("#rollingselection").change(function() {
		var timeToToggle = 100;
		var all = $(this).children();
		var typeChosen = $(this).find(":selected").prop('id');
		for (var i = 0, option; option = all[i]; i++) {
			$("#rolling"+option.id).hide();
		}
		$("#rolling"+typeChosen).show();
		if (typeChosen == "averagedata") {
        	$(".minifilemanage").animate({ opacity: 0 }, timeToToggle);
		}
		else {
        	$(".minifilemanage").animate({ opacity: 1 }, timeToToggle);
		}
	});

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

	$("#prettydatafileselect").click(function() {
		$("#datafileselect").click();
	});
});