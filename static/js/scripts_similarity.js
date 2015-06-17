$(function() {

	// Hide unnecessary divs for DTM
	$("#dtm-div").hide();
	$("#normalize-options").hide();
	$("#culling-options").hide();
	$("#temp-label-div").css("position","relative").css("left","-10px").css("top","0px");

	// Initialize the Bootstrap multiselect plugin
	$('#simFileSelect').multiselect();

	$("form").submit(function(){
		if ($(".minifilepreview.enabled").length < 1) {
			$("#simsubmiterrormessage").show().fadeOut(3000,"easeInOutCubic");
			return false;
		}
	});

	// Code to try and make the tokenize box look pretty on simQ page.  Only works in firefox? Makes templabels disappear in chromium
	// var brow, usrAG = navigator.userAgent;		// Catch browser info
	// if (usrAG.indexOf("Firefox") > -1) {        // if 'firefox' in browser name then apply this style stuff
	// 	$("#temp-label-div").css("position","relative").css("top","-126px").css("left","-10px");
	// 	$("#analyze-advanced").css("max-height","150px").css("overflow","hidden");

	// 	$("input[name='tokenType']").click(function(){
	// 		if ($(this).val() == 'word'){
	// 			$("#temp-label-div").css("top","-126px");
	// 		} else {
	// 			$("#temp-label-div").css("top","-161px");
	// 		}
	// 	});
	// } 

	$('#getsims').click(function () {
		return true;
	});

	// Doesn't work?
	// $("form").submit(function () {
	// 	if ($("#uploadname").val() == '') {
	// 		//$('#error-message').text("You must select a comparison file!");
	// 		$('#error-message').show().fadeOut(1200, "easeInOutCubic");
	// 		return false;
	// 	}
	// 	else {
	// 		return true;
	// 	}

	// });

	function createList() {

		mytable = $('<table></table>').attr({id: "basicTable"});

		// title row
		var titleRow = $('<tr></tr>').appendTo(mytable);
		$('<td></td>').text("Rank").appendTo(titleRow);
		$('<td></td>').text("Filename").appendTo(titleRow);
		$('<td></td>').text("Cosine Similarity").appendTo(titleRow);

		// rankings
		var rows = (docsListScore.length - 1);
		var cols = 3;
		var tr = [];
		for (var i = 0; i < rows; i++) {
			var row = $('<tr></tr>').appendTo(mytable);
			for (var j = 0; j < cols; j++) {

				if (j == 0) {
					$('<td></td>').text(i + 1).appendTo(row);
				} else if (j == 1) {
					$('<td></td>').text(docsListName[i]).appendTo(row);
				} else {
					$('<td></td>').text(docsListScore[i]).appendTo(row);
				}
			}//for
		}//for

		mytable.appendTo("#simstable");
	}

	createList();

});
