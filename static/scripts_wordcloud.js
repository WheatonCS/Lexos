$(function() {
	// Spinner Functionality
	$( "#minlength" ).spinner({
		step: 1,
		min: 0
	});
	$( "#graphsize" ).spinner({
		step: 10,
		min: 100,
		max: 3000
	});
	
	// Multiselect Dropdown Functionality
	$("#segmentlist").multiselect({
		noneSelectedText: "Select Segments",
		selectedText: "# of # checked"		
	});

	// Loop through the token list, already filtered, to create a JavaScript array
	var tokens = [];

	$.each($(".words"), function(index, value) {
		//alert($(value).val());
		tokens.push($(value).val());
	});
    //alert(tokens);
});



// Word Cloud - by Scott Kleinman
// Word Cloud is based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html.
