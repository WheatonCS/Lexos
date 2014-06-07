$(function() {
	function updateTokenizeCheckbox() {
		if ($('input[type=radio][name=tokenType][value=word]').attr('checked')) {
			console.log('ayy');
			$('input[type=checkbox][name=inWordsOnly]').attr('disabled', 'true');
			$('input[type=checkbox][name=inWordsOnly]').parent('label').addClass('disabled');
		}
		else {
			console.log('no');
			$('input[type=checkbox][name=inWordsOnly]').removeAttr('disabled');
			$('input[type=checkbox][name=inWordsOnly]').parent('label').removeClass('disabled');
		}
	}

	$('input[type=radio][name=tokenType]').click(updateTokenizeCheckbox);

	updateTokenizeCheckbox();
});