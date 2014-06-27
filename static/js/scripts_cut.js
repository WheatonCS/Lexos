function nocuttingvalue() {
	// var cuttingValues = $(".cuttingValue")
	// var numTotalCutValues = cuttingValues.length;

	// var numEmptyCutValues = cuttingValues.filter(function(){
	// 	return this.value == '';
	// }).length;
	// var numZeroCutValues = cuttingValues.filter(function() {
	// 	return this.value == '0'
	// }).length;
	// var numOneCutValues = cuttingValues.filter(function() {
	// 	return this.value == '1'
	// }).length;

	if ($("#overallcutvalue").val() == '') {
		$('#error-message').text("You must provide a default cutting value!");
		$('#error-message').show().fadeOut(1200, "easeInOutCubic");
		return false;
	}
	// else if ( numZeroCutValues > 0 ) {
	// 	$("#cutsubmiterrormessage2").show().fadeOut(1200, "easeInOutCubic");
	// 	return false;
	// }
}

$(function() {

/*	$("form").submit(function() {
		var overallcutvalue = $("#overallcutvalue").val();
		var cutOverlap = $("#cutOverlap").val();
		var cutLastProp = $("#cutLastProp").val();

		if ((Math.abs(Math.round(overallcutvalue)) != overallcutvalue) && (overallcutvalue != '')){
			console.log("first if");
			$('#error-message').text("Invalid input! Make sure all inputs are integers!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if ((Math.abs(Math.round(cutOverlap)) != cutOverlap) && (cutOverlap != '') && (typeof cutOverlap != 'undefined')) {
			console.log("cutOverlap: "+ cutOverlap);
			console.log("second if");
			$('#error-message').text("Invalid input! Make sure all inputs are integers!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else if((Math.abs(Math.round(cutLastProp)) != cutLastProp) && (cutLastProp != '') && (typeof(cutLastProp) != 'undefined')) {
			console.log("third if");
			$('#error-message').text("Invalid input! Make sure all inputs are integers!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;	
		}
		else {
			return true;
		}
	});*/

	var previewContentHeight = $('.filecontents').height();
	var timeToToggle = 150;
	$(".sizeradio").click( function() {
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
		cuttingValueLabel.text("Chunk Size:");

		$(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
				.animate({ opacity: 1 }, timeToToggle)
				.find('.lastprop-input').prop('disabled', false);

		$(this).parents('.cuttingoptionswrapper').find('.overlap-div')
				.animate({ opacity: 1 }, timeToToggle)
				.find('.overlap-input').prop('disabled', false);
	});

	$(".numberradio").click( function() {
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
		cuttingValueLabel.text("Number of Chunks:");

		$(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
				.animate({ opacity: 0.2 }, timeToToggle)
				.find('.lastprop-input').prop('disabled', true);

		$(this).parents('.cuttingoptionswrapper').find('.overlap-div')
				.animate({ opacity: 0.2 }, timeToToggle)
				.find('.overlap-input').prop('disabled', true);
	});


	// $(".textinput").keypress(function(evt) {
	// 	var theEvent = evt || window.event;
	// 	var key = theEvent.keyCode || theEvent.which;
	// 	if (key != 8) {
	// 		key = String.fromCharCode( key );
	// 		var regex = /[0-9]|\./;
	// 		if( !regex.test(key) ) {
	// 			theEvent.returnValue = false;
	// 			if(theEvent.preventDefault) theEvent.preventDefault();
	// 		}
	// 	}
	// });


	var timeToToggle = 300;
	$(".indivcutbuttons").click( function() {
		var toggleDiv = $(this).parents('.individualpreviewwrapper').find('.cuttingoptionswrapper');
		toggleDiv.slideToggle(timeToToggle);
	});

	$("form").submit(function() {
		return nocuttingvalue();
	});

	if ($("#supercuttingmode").prop('checked')) {
		$("#supercuttingmodemessage").show().fadeOut(3000, "easeInOutQuint");
	}
});