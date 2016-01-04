function errorHandler() {

	if ($("#cutByMS").is(":checked")){
		if ($("#MScutWord").val() == ''){
			$('#error-message').text("You must provide a string to cut on!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			$("#status-prepare").hide()
			return false;
		} else {
			return true;
		}
	} else {

		if ($("#overallcutvalue").val() == '') {
			$('#error-message').text("You must provide a default cutting value!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			$("#status-prepare").hide()
			return false;
		}
		else {
			var overallcutvalue = parseInt($("#overallcutvalue").val());
			var overallOverlapValue = parseInt($("#overallOverlapValue").val());
			var individualOverlap = parseInt($("#individualOverlap").val());
			var individualCutValue = $("#individualCutValue").val();
			
			if((Math.abs(Math.round(overallcutvalue)) != overallcutvalue) || overallcutvalue == 0) {
				$('#error-message').text("Default cutting: Invalid segment size!");
				$('#error-message').show().fadeOut(3000, "easeInOutCubic");
				$("#status-prepare").hide()
				return false;
			}

			if ((overallcutvalue <= overallOverlapValue) || (Math.abs(Math.round(overallOverlapValue)) != overallOverlapValue)) {
				$('#error-message').text("Default cutting: Invalid overlap value!");
				$('#error-message').show().fadeOut(3000, "easeInOutCubic");
				$("#status-prepare").hide()
				return false;
			}

			if (individualCutValue != '') {
				individualCutValue = parseInt(individualCutValue);
				if ((Math.abs(Math.round(individualCutValue)) != individualCutValue)) {
					$('#error-message').text("Individual cutting: Invalid segment size!");
					$('#error-message').show().fadeOut(3000, "easeInOutCubic");
					$("#status-prepare").hide()
					return false;
				}
				if ((individualCutValue <= individualOverlap) || (Math.abs(Math.round(individualOverlap)) != individualOverlap)) {
					$('#error-message').text("Individual cutting: Invalid overlap value!");
					$('#error-message').show().fadeOut(3000, "easeInOutCubic");
					$("#status-prepare").hide()
					return false;
				}
			}

		} 
	}
};


$(function() {

	$("#actions").addClass("actions-cut");
	
	// Toggle cutting options when radio buttons with different classes are clicked
	var timeToToggle = 150;
	$(".sizeradio").click( function() {
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
		cuttingValueLabel.text("Segment Size:");

		$(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
				.animate({ opacity: 1 }, timeToToggle)
				.find('.lastprop-input').prop('disabled', false);

		$(this).parents('.cuttingoptionswrapper').find('.overlap-div')
				.animate({ opacity: 1 }, timeToToggle)
				.find('.overlap-input').prop('disabled', false);
	});

	$(".numberradio").click( function() {
		var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text');
		cuttingValueLabel.text("Number of Segments:");

		$(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
				.animate({ opacity: 0.2 }, timeToToggle)
				.find('.lastprop-input').prop('disabled', true);

		$(this).parents('.cuttingoptionswrapper').find('.overlap-div')
				.animate({ opacity: 0.2 }, timeToToggle)
				.find('.overlap-input').prop('disabled', true);
	});

	// Toggle individual cut options 
	$(".indivcutbuttons").click( function() {
		var toggleDiv = $(this).parents('.individualpreviewwrapper').find('.cuttingoptionswrapper');
		toggleDiv.toggleClass("hidden");
		// slideToggle() only works if the div is first set to 'display:none'
		//toggleDiv.slideToggle(timeToToggle);
	});

	// Call error handler when submit buttons are clicked
	$("form").submit(function() {
		return errorHandler();
	});

	// Toggle milestone options
	function showMilestoneOptions(){
		if ($("#cutByMS").is(":checked")){
			$("#MSoptspan").show();
			$("#cuttingdiv").hide();
		} else {
			$("#MSoptspan").hide();
			$("#cuttingdiv").show();
		}
	}

	$("#cutByMS").click(showMilestoneOptions);

	showMilestoneOptions();

	$(".indivMS").click( function() {
		if ($(this).is(":checked")) {
			$(this).parents("#cutByMSdiv").filter(":first").children("#MSoptspan").show();
			$(this).parents("#cutByMSdiv").filter(":first")
			.parents(".cuttingoptionswrapper").find(".individcut").hide();
		} else {
			$(this).parents("#cutByMSdiv").filter(":first").children("#MSoptspan").hide();
			$(this).parents("#cutByMSdiv").filter(":first")
			.parents(".cuttingoptionswrapper").find(".individcut").show();
		}

	});

});