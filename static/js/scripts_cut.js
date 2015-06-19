function nocuttingvalue() {
	if ($("#cutByMS").is(":checked")){
		if ($("#MScutWord").val == ''){
			$('#error-message').text("You must provide a string to cut on!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		} else {
			return true;
		}
	} else {
		if ($("#overallcutvalue").val() == '') {
			$('#error-message').text("You must provide a default cutting value!");
			$('#error-message').show().fadeOut(3000, "easeInOutCubic");
			return false;
		}
		else {
			var overallcutvalue = $("overallcutvalue").val();
			var overallOverlapValue = $("overallOverlapValue").val();
			var individualCutValue = $("individualCutValue").val();
			var individualOverlap = $("individualOverlap").val();

			if((Math.abs(Math.round(overallcutvalue)) != overallcutvalue) || overallcutvalue == 0) {
				$('#error-message').text("Default cutting: Invalid segment size!");
				$('#error-message').show().fadeOut(3000, "easeInOutCubic");
				return false;
			}

			if ((overallcutvalue <= overallOverlapValue) || (Math.abs(Math.round(overallOverlapValue)) != overallOverlapValue)) {
				$('#error-message').text("Default cutting: Invalid overlap value!");
				$('#error-message').show().fadeOut(3000, "easeInOutCubic");
				return false;
			}

			if (individualCutValue != '') {
				if ((Math.abs(Math.round(individualCutValue)) != individualCutValue)) {
					$('#error-message').text("Individual cutting: Invalid segment size!");
					$('#error-message').show().fadeOut(3000, "easeInOutCubic");
					return false;
				}
				if ((individualCutValue <= individualOverlap) || (Math.abs(Math.round(individualOverlap)) != individualOverlap)) {
					$('#error-message').text("Individual cutting: Invalid overlap value!");
					$('#error-message').show().fadeOut(3000, "easeInOutCubic");
					return false;
				}
			}

			return true;
		}
	}
}

$(function() {
	if ($("input[name=cutType]:checked").val()){
		$("input[name=cutType][value=words]").prop("checked",true)
	}


	var previewContentHeight = $('.filecontents').height();
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
		cuttingValueLabel.text("Number of segments:");

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
			$(this).parents("#cutByMSdiv").filter(":first").parents(".cuttingoptionswrapper").find(".individcut").hide();
		} else {
			$(this).parents("#cutByMSdiv").filter(":first").children("#MSoptspan").hide();
			$(this).parents("#cutByMSdiv").filter(":first").parents(".cuttingoptionswrapper").find(".individcut").show();
		}

	});

});