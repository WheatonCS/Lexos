$(function() {
	var timeToToggle = 300;
	$("#stopwords").click( function() {
		$("#stopwordinput").slideToggle(timeToToggle);
	});
	$("#prettystopwordsupload").click( function() {
		$("#swfileselect").click();
	});


	$("#lemmas").click( function() {
		$("#lemmainput").slideToggle(timeToToggle);
	});
	$("#prettylemmasupload").click( function() {
		$("#lemmafileselect").click();
	});


	$("#consolidations").click( function() {
		$("#consolidationsinput").slideToggle(timeToToggle);
	});
	$("#prettyconsolidationsupload").click( function() {
		$("#consolidationsfileselect").click();
	});


	// $("#stopwords").click( function() {
	// 	$("#stopwordmanualinput").animate({width: 'toggle'}, timeToToggle);
	// 	$("#prettystopwordsupload").fadeToggle(timeToToggle);
	// });
	// $("#prettystopwordsupload").click( function() {
	// 	$("#swfileselect").click();
	// });

	// $("#specialchars").click( function() {
	// 	$("#box-specialchars").slideToggle(timeToToggle);
	// });
});

$(function() {
	var timeToToggle = 100;
	$("#punctbox").click( function() {
		$("#apos").fadeToggle(timeToToggle);
		$("#hyph").fadeToggle(timeToToggle);
	});
});

$(function() {
	$(document).tooltip({
		position:{
			relative: true,
			at: "center top-5", // location on the mouse
								// Negative horizontal is left, negative vertical is up 
			my: "center bottom",// location on the tooltip popup window
			collision: "fit"
		}

	});
});