$(function() {
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
});