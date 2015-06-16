$(function() {
	// Config the toggle when create new DTM is supposed to be toggled on
	function toggleCreateNew() {
		$("#toggle-division-bar").css("right", "80%");
		$(".toggle").removeClass('btn-primary')
					.addClass('btn-default')
					.html("Create New DTM")
					.css({"right": "-5%"});
		$(".toggle-dtm").css("background-color", "#2ECC71");
		$("#newDTM").attr('checked', true);
		$("#oldDTM").attr('checked', false);
	}

	// Config the toggle when use old DTM is supposed to be toggled on
	function toggleUseOld() {
		$("#toggle-division-bar").css("right", "0");
		$(".toggle").removeClass('btn-default')
					.addClass('btn-primary')
					.html("Use Existing DTM")
					.css("right", "15%");
		$(".toggle-dtm").css("background-color", "#16A085");
		$("#oldDTM").attr('checked', true);
		$("#newDTM").attr('checked', false);
	}

	// Initialize toggle configurations
	$(".dtm-option").css("display", "none");
	$(".toggle-dtm").bind("click");

	if ($(".toggle").hasClass('btn-primary')) {
		toggleUseOld();
	}else{
		toggleCreateNew();
	}

	// Toggle the button when button onclick
	$(".toggle-dtm").click(function(){
		if ($(".toggle").hasClass('btn-primary')) {
			toggleCreateNew();
		}else{
			toggleUseOld();
		}
	});

	// Disable the toggle when no DTM exists
	$(".tokenize-div, .normalize-div, .culling-div, #modifylabels").click(function(){
		toggleCreateNew();
		$(".toggle-dtm").unbind("click")
						.css("background-color", "gray");
	});

	// Handle exceptions before form being submitted
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
			if ($("#culling").is(":checked")){
				$("#temp-label-div").css('max-height','221px');
				$("#modifylabels").css('max-height','160px');
			} else {
				$("#temp-label-div").css('max-height','191px');
				$("#modifylabels").css('max-height','130px');
			}
		} else {
			if ($("#culling").is(":checked")){
				$("#temp-label-div").css('max-height','191px');
				$("#modifylabels").css('max-height','130px');
			} else {
				$("#temp-label-div").css('max-height','161px');
				$("#modifylabels").css('max-height','100px');
			}
			$('span[id=mfwnumber-input]').hide();
		}
	}

	$('input[type=checkbox][name=mfwcheckbox]').click(updateMFWinput);

	updateMFWinput();

	function updatecullinput() {
		if ($("#culling").is(":checked")){
			$('span[id=cullnumber-input]').show();
			if ($("#MFW").is(":checked")){
				$("#temp-label-div").css('max-height','221px');
				$("#modifylabels").css('max-height','160px');
			} else {
				$("#temp-label-div").css('max-height','191px');
				$("#modifylabels").css('max-height','130px');
			}
		} else {
			if ($("#MFW").is(":checked")){
				$("#temp-label-div").css('max-height','191px');
				$("#modifylabels").css('max-height','130px');
			} else {
				$("#temp-label-div").css('max-height','161px');
				$("#modifylabels").css('max-height','100px');
			}
			$('span[id=cullnumber-input]').hide();
		}
	}

	$('input[type=checkbox][name=cullcheckbox]').click(updatecullinput);

	updatecullinput();

	// Change position of submit div while scrolling the window
	var timer;
	var buttonsFixed = false;
	var buttons = $('#analyze-submit');

	$(window).scroll(function(){
		// Timer stuff
		if (timer) {
			clearTimeout(timer);
		}
		// Timer to throttle the scroll event so it doesn't happen too often
		timer = setTimeout(function(){
			var scrollBottom = $(window).scrollTop() + $(window).height();
			var scrollTop = $(window).scrollTop();

			// if bottom of scroll window at the footer, allow buttons to rejoin page as it goes by
			if ((buttonsFixed && (scrollBottom >= ($('footer').offset().top))) || scrollTop == 0) {
				// console.log("Scroll bottom hit footer! On the way down");
				buttons.removeClass("fixed");
				buttonsFixed = false;
			}

			// if bottom of scroll window at the footer, fix button to the screen
			if (!buttonsFixed && (scrollBottom < ($('footer').offset().top)) && scrollTop != 0) {
				// console.log("Scroll bottom hit footer! On the way up");
				buttons.addClass("fixed");
				buttonsFixed = true;
			}
		}, 10);
	});

	$(window).scroll(); // Call a dummy scroll event after everything is loaded.
});
