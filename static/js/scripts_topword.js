$(function() {
	// Hide unnecessary div for DTM
	$("#normalize-options").css({"visibility":"hidden"});
	$("#temp-label-div").css("position", "relative").css("left","-6px").css("top","0px");

	// display/hide expandable divs (Define Groups div) here
	function updateGroupOptionDiv() {
		$choice = $(".show-options div").siblings('input');
		$.each($choice, function () {
			if ($(this).is(':checked')) {
				$(this).siblings('div').show();
			} else
				$(this).siblings('div').hide();
		})
	}
	
	updateGroupOptionDiv();
	$(".groupOption-div").click(function(){
		updateGroupOptionDiv();
	});

	// Display a new div based on choosing proportional Z-test or not
	function updateTestMethodDiv() {
		if ($("#pz").is(':checked')) {
			$(".test-input-div").removeClass("hidden");
		} else {
			$(".test-input-div").addClass("hidden");
		}
	}

	updateTestMethodDiv();
	$(".testMethod-div").click(function(){
		updateTestMethodDiv();
	});

	// Dynamically change the upper and lower bounds based on user inputs (Proportional Counts)
	$("#upperboundPC").click(function () {
		$(this).context.min = $("#lowerboundPC").val();
		$("#upperboundRC, #lowerboundRC").val(0);
	});

	$("#lowerboundPC").click(function () {
		$(this).context.max = $("#upperboundPC").val();
		$("#upperboundRC, #lowerboundRC").val(0);
	});

	// Reset proportional counts input fields while raw counts is chosed
	$("#upperboundRC, #lowerboundRC").click(function () {
		$("#upperboundPC, #lowerboundPC").val(0);
	});

	// Handle exceptions before submitting the form
	$("form").submit(function () {
		if ( classNum < 2) {
			$('#error-message').text("You must have at least two classes exist to proceed!");
			$('#error-message').show().fadeOut(3000);
			return false;
		}
	});
});
