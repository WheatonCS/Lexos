$(function() {
	// Add initial classes for checkboxes for icons
	$.each($('input[type=checkbox]'), function() {
		$(this).parent('label').addClass('icon-checkbox');
	});
	// Add initial classes for radio buttons for icons
	$.each($('input[type=radio]'), function() {
		$(this).parent('label').addClass('icon-radio');
	});

	// Add initial classes for checkboxes based on initial state (checked or unchecked)
	$.each($('input[type=checkbox]'), function() {
		if (this.checked)
			$(this).parent('label.icon-checkbox').addClass('checked');
		else
			$(this).parent('label.icon-checkbox').removeClass('checked');
	});

	// Add initial classes for radios based on initial state (checked or unchecked)
	$.each($('input[type=radio]'), function() {
		if (this.checked)
			$(this).parent('label.icon-radio').addClass('checked');
		else
			$(this).parent('label.icon-radio').removeClass('checked');
	});

	// Toggle the state on click for checkboxes
	$('input[type=checkbox]').click(function() {
		$(this).parent('label.icon-checkbox').toggleClass('checked');
	});

	// Toggle the state on click for radio buttons
	$('input[type=radio]').click(function() {
		var name = $(this).attr('name');

		$('input[type=radio][name='+name+']').parent('label.icon-radio').removeClass('checked');
		$(this).parent('label.icon-radio').addClass('checked');

		// $(this).parent('label.icon-radio').siblings('label.icon-radio').removeClass('checked');
		// $(this).parent('label.icon-radio').addClass('checked');
	});
});