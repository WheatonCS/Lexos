$(function() {
	var timeToToggle = 300;
	$("#labeleditting").click( function() {
		$("#modifylabels").slideToggle(timeToToggle);
	});

	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});
});