$(function() {

	$("form").submit(function() {
		var tokenSize = $("#tokenSize").val();
		if (Math.abs(Math.round(tokenSize)) != tokenSize){
			$('#error-message').text("Invalid input! Make sure number of grams is an integer!");
			$('#error-message').show().fadeOut(1200, "easeInOutCubic");
			return false;
		}
		else {
			return true;
		}
	});

	function updateTokenizeCheckbox() {
		if ($("#tokenByWords").is(":checked")) {
			$("#inWordsOnly").hide();
		}
		else {
			$("#inWordsOnly").show();
		}
	}

	$("input[type=radio][name=tokenType]").click(updateTokenizeCheckbox);

	updateTokenizeCheckbox();

	function updateNorm() {
		if ($("#normalizeTypeRaw").is(":checked") || $("#normalizeTypeFreq").is(":checked") ) {
			$("#tfidfspan").hide();
		}
		else {
			$("#tfidfspan").show();
		}
	}

	$('input[type=radio][name=normalizeType]').click(updateNorm);

	updateNorm();

	function updateMFWinput() {
		if ($("#MFW").is(":checked")){
			$('span[id=mfwnumber-input]').show();
		} else {
			$('span[id=mfwnumber-input]').hide();
		}
	}

	$('input[type=checkbox][name=mfwcheckbox]').click(updateMFWinput);

	updateMFWinput();

	function updatecullinput() {
		if ($("#culling").is(":checked")){
			$('span[id=cullnumber-input]').show();
		} else {
			$('span[id=cullnumber-input]').hide();
		}
	}

	$('input[type=checkbox][name=cullcheckbox]').click(updatecullinput);

	updatecullinput();

	$(".toggle-dtm").click(function(){
		if ($(".toggle").hasClass('btn-primary')) {
			$("#toggle-division-bar").css("right", "80%");
			$(".toggle").removeClass('btn-primary')
						.addClass('btn-default')
						.html("Create New DTM")
						.css({"right": "-5%"});
			$(".toggle-dtm").css("background-color", "#2ECC71");
			$("#newDTM").attr('checked', true);
			$("#oldDTM").attr('checked', false);

		}else{
			$("#toggle-division-bar").css("right", "0");
			$(".toggle").removeClass('btn-default')
						.addClass('btn-primary')
						.html("Use Existing DTM")
						.css("right", "15%");
			$(".toggle-dtm").css("background-color", "#16A085");
			$("#oldDTM").attr('checked', true);
			$("#newDTM").attr('checked', false);
		}
	});
});

$(document).ready(function() {
	$(".dtm-option").css("display", "none");

	if ($(".toggle").hasClass('btn-primary')) {
		$("#toggle-division-bar").css("right", "0");
		$(".toggle").html("Use Existing DTM")
					.css("right", "15%");
		$(".toggle-dtm").css("background-color", "#16A085");
		$("#oldDTM").attr('checked', true);
		$("#newDTM").attr('checked', false);
			

	}else{
		$("#toggle-division-bar").css("right", "80%");
		$(".toggle").html("Create New DTM")
					.css("right", "-5%");
		$(".toggle-dtm").css("background-color", "#2ECC71");
		$("#newDTM").attr('checked', true);
		$("#oldDTM").attr('checked', false);
	}
}); 
