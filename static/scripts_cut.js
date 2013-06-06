function nocuttingvalue() {
	var cuttingValues = $(".cuttingValue")

	var numTotalCutValues = cuttingValues.length;
	var numEmptyCutValues = cuttingValues.filter(function(){
		return this.value == '';
	}).length;
	var numZeroCutValues = cuttingValues.filter(function() {
		return this.value == '0'
	}).length;
	var numOneCutValues = cuttingValues.filter(function() {
		return this.value == '1'
	}).length;

	if ($("#overallCutValue").val() == '' && numEmptyCutValues > 1) {
		alert('Please fill out enough segment value fields');
	}
	else if ( numZeroCutValues > 0 ) {
		alert('You cannot enter a value of 0 for a segment value');
	}
	else if ( numTotalCutValues == 2 && $("#overallCutValue").val() == '1' && numOneCutValues+numEmptyCutValues > 1) {
		alert('A dendrogram cannot be made with one segment');
	}
	else {
		return true;
	}
	return false;
}

$(function() {
    $(document).tooltip({
        position:{
            relative: true,
            at: "center center", // location on the mouse
                                // Negative horizontal is left, negative vertical is up 
            my: "left+20 center"// location on the tooltip popup window
        }

    });
});

$(function () {
    var timeToToggle = 150;
    $(".sizeradio").click( function() {
        var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cuttingoptionslabel');
        cuttingValueLabel.text("Segment Size:");

        var lastproportiondiv = $(this).parents('.cuttingoptionswrapper').find('.lastproptableslot');
        lastproportiondiv.fadeIn(timeToToggle);
        lastproportiondiv.find('.lastpropinput').prop('disabled', false);
    });


    $(".numberradio").click( function() {
        var cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cuttingoptionslabel');
        cuttingValueLabel.text("Number of Segments:");

        var lastproportiondiv = $(this).parents('.cuttingoptionswrapper').find('.lastproptableslot');
        lastproportiondiv.fadeOut(timeToToggle);
        lastproportiondiv.find('.lastpropinput').prop('disabled', false);
    });


// = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    $(".indivcutbuttons").click( function() {
        var toggleDiv = $(this).parents('.individualpreviewwrapper').find('.cuttingoptionswrapper');
        toggleDiv.slideToggle(timeToToggle);
    });

});