function nocuttingvalue() {
	if ($("#overallcutvalue").val() == '') {
		$('#error-message').text("You must provide a default cutting value!");
		$('#error-message').show().fadeOut(1200, "easeInOutCubic");
		return false;
	}
	else {
		overallcutvalue = document.getElementById("overallcutvalue").value;
		overallOverlapValue = document.getElementById("overallOverlapValue").value;
		individualCutValue = document.getElementById("individualCutValue").value;
		individualOverlap = document.getElementById("individualOverlap").value;

		if((Math.abs(Math.round(overallcutvalue)) != overallcutvalue) || (Math.abs(Math.round(individualCutValue)) != individualCutValue)) {
			$('#error-message').text("Invalid chunk size!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}

		if ((overallcutvalue < overallOverlapValue) || (Math.abs(Math.round(overallOverlapValue)) != overallOverlapValue) || (Math.abs(Math.round(individualOverlap)) != individualOverlap)) {
			$('#error-message').text("Invalid overlap value!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}

		return true;
	}
}

$(function() {
	var previewContentHeight = $('.filecontents').height();
	var timeToToggle = 150;
	$(".sizeradio").click( function() {
		alert("in sizeradio");
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
		alert("in numberradio");
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
		cuttingValueLabel.text("Number of Chunks:");

		$(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
				.animate({ opacity: 0.2 }, timeToToggle)
				.find('.lastprop-input').prop('disabled', true);

		$(this).parents('.cuttingoptionswrapper').find('.overlap-div')
				.animate({ opacity: 0.2 }, timeToToggle)
				.find('.overlap-input').prop('disabled', true);
	});

	var timeToToggle = 300;
	$(".indivcutbuttons").click( function() {
		var toggleDiv = $(this).parents('.individualpreviewwrapper').find('.cuttingoptionswrapper');
		toggleDiv.slideToggle(timeToToggle);
	});

	$("form").submit(function() {
		return nocuttingvalue();
	});

/*	if ($("#supercuttingmode").prop('checked')) {
		$("#supercuttingmodemessage").show().fadeOut(3000, "easeInOutQuint");
	}*/
});