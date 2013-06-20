$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});

	$("#rollingselection").change(function() {
		var all = $(this).children();
		var typeChosen = $(this).find(":selected").prop('id');
		for (var i = 0, option; option = all[i]; i++) {
			$("#rolling"+option.id).hide();
		}
		$("#rolling"+typeChosen).show();
	});

	$(".minifilepreview").click(function() {
		$(this).siblings(".minifilepreview").removeClass('enabled');
		$(this).addClass('enabled');
		$("#filetorollinganalyze").val($(this).prop('id'));
	});

	$("#prettydatafileselect").click(function() {
		$("#datafileselect").click();
	});
});