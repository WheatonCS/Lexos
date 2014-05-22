function nocuttingvalue() {
	var cuttingValues = $(".cuttingValue")
	var numTotalCutValues = cuttingValues.length;
	var numEmptyCutValues = cuttingValues.filter(function(){
		return this.value == '';
	}).length;
	var numZeroCutValues = cuttingValues.filter(function() {
		return this.value == '0'
	}).length;
	var numOneCutValues = cuttingValues.filter(function() {
		return this.value == '1'
	}).length;

	if ($("#overallcutvalue").val() == '' && numEmptyCutValues > 1) {
		$("#cutsubmiterrormessage1").show().fadeOut(1200, "easeInOutCubic");
		return false;
	}
	else if ( numZeroCutValues > 0 ) {
		$("#cutsubmiterrormessage2").show().fadeOut(1200, "easeInOutCubic");
		return false;
	}
}

$(function() {
	var previewContentHeight = $('.filecontents').height();
	var timeToToggle = 150;
	$(".sizeradio").click( function() {
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cuttingoptionslabel');
		cuttingValueLabel.text("Segment Size:");

		var lastproportiondiv = $(this).parents('.cuttingoptionswrapper').find('.lastpropdiv');
		lastproportiondiv.animate({ opacity: 1 }, timeToToggle);
		lastproportiondiv.find('.lastpropinput').prop('disabled', false);
	});

	$(".numberradio").click( function() {
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cuttingoptionslabel');
		cuttingValueLabel.text("Number of Segments:");

		var lastproportiondiv = $(this).parents('.cuttingoptionswrapper').find('.lastpropdiv');
		lastproportiondiv.animate({ opacity: 0 }, timeToToggle);
		lastproportiondiv.find('.lastpropinput').prop('disabled', true);
	});


	$(".textinput").keypress(function(evt) {
		var theEvent = evt || window.event;
		var key = theEvent.keyCode || theEvent.which;
		if (key != 8) {
			key = String.fromCharCode( key );
			var regex = /[0-9]|\./;
			if( !regex.test(key) ) {
				theEvent.returnValue = false;
				if(theEvent.preventDefault) theEvent.preventDefault();
			}
		}
	});


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