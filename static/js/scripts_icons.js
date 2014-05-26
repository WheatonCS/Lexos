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

	// Toggle the state on click for checkboxes
	$('input[type=radio]').click(function() {
		$(this).parent('label.icon-radio').siblings('label.icon-radio').removeClass('checked');
		$(this).parent('label.icon-radio').addClass('checked');
	});


	// Gray out all disabled inputs
	$.each($('input'), function() {
		if ($(this).prop('disabled')) {
			$(this).addClass('disabled');
			$(this).parent('label').addClass('disabled');
		}
	});
});