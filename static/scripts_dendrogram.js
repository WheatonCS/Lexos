$(function() {

	var timeToToggle = 300;
	$("#labeleditting").click( function() {
		$("#modifylabels").slideToggle(timeToToggle);
	});
});

function attemptdendro() {
	var activeFiles = $('.filenames').length;
	if (activeFiles == 0) {
		alert("There are currently no active files.");
	}
	else if (activeFiles == 1) {
		alert("A dendrogram requires at least 2 active files to be created (Currently 1 active file).");
	}
	else {
		return true;
	}
	return false;
}

$(function() {
	$('#getdendro').click( function() {
		return attemptdendro();
	});
});