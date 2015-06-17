$(function() {
	// Hide unnecessary div for DTM
	$("#normalize-options").hide();

	// Disable dtm toggle when matrix
	if (matrixExist === 0){
		$(".toggle-dtm").unbind("click")
						.css("background-color", "gray");
	}

	// display/hide expandable divs (Define Groups div) here
	$(".groupOption-div").click(function() {
		$choice = $(".show-options div").siblings('input');
		$.each($choice, function(){
			if ($(this).is(':checked')) {
				$(this).siblings('div').show();
			} else
				$(this).siblings('div').hide();
		});
	});

	// Dynamically change the upper and lower bounds based on user inputs
	$("#upperboundPC").click(function() {
		$(this).context.min = $("#lowerboundPC").val();
	});

	$("#lowerboundPC").click(function() {
		$(this).context.max = $("#upperboundPC").val();
	});

	
	function updateTokenizeCheckbox() {
		$('input[type=radio][name=normalizeType]').attr('disabled', 'true');
		$('input[type=radio][name=normalizeType]').parent('label').addClass('disabled');
	}

	updateTokenizeCheckbox();

});
