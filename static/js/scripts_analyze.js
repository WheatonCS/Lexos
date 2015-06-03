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
		if ($('input[type=radio][name=tokenType][value=word]').attr('checked')) {
			$('input[type=checkbox][name=inWordsOnly]').attr('disabled', 'true');
			$('input[type=checkbox][name=inWordsOnly]').parent('label').addClass('disabled');
		}
		else {
			$('input[type=checkbox][name=inWordsOnly]').removeAttr('disabled');
			$('input[type=checkbox][name=inWordsOnly]').parent('label').removeClass('disabled');
		}
	}

	$('input[type=radio][name=tokenType]').click(updateTokenizeCheckbox);

	updateTokenizeCheckbox();

	function updateNorm() {
		if ($('input[type=radio][name=normalizeType][value=raw]').attr('checked')) {
			document.getElementById("tfidfNorm").style.visibility = "hidden";
		}
		else if ($('input[type=radio][name=normalizeType][value=freq]').attr('checked')){
			document.getElementById("tfidfNorm").style.visibility = "hidden";
		}
		else {
			document.getElementById("tfidfNorm").style.visibility = "visible";
		}
	}

	$('input[type=radio][name=normalizeType]').click(updateNorm);

	updateNorm();


	$(".toggle-dtm").click(function(){
		if ($(".toggle").hasClass('btn-primary')) {
			$("#toggle-division-bar").css("right", "80%");
			$(".toggle").removeClass('btn-primary')
						.addClass('btn-default')
						.html("Create New DTM")
						.css({"right": "-5%"});
			$(".toggle-dtm").css("background-color", "#2ECC71");

		}else{
			$("#toggle-division-bar").css("right", "0");
			$(".toggle").removeClass('btn-default')
						.addClass('btn-primary')
						.html("Use Existing DTM")
						.css("right", "15%");
			$(".toggle-dtm").css("background-color", "#16A085");
		}
	});
});

$(document).ready(function() {
	if ($(".toggle").hasClass('btn-primary')) {
		$("#toggle-division-bar").css("right", "0");
		$(".toggle").html("Use Existing DTM")
					.css("right", "15%");
		$(".toggle-dtm").css("background-color", "#16A085");
			

	}else{
		$("#toggle-division-bar").css("right", "80%");
		$(".toggle").html("Create New DTM")
					.css("right", "-5%");
		$(".toggle-dtm").css("background-color", "#2ECC71");
	}
}); 
