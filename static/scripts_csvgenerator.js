$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});

	var timeToToggle = 300;
	$("#labeleditting").click( function() {
		$("#modifylabels").slideToggle(timeToToggle);
	});
});