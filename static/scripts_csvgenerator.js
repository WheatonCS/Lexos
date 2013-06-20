$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});
});