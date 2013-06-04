function nocuttingvalue() {
    if ($("#overallCutValue").val() == '') {
        var numEmptyCutValues = $(".cuttingValue").filter(function(){ return this.value == '' }).length
        if ( numEmptyCutValues > 1 ) {
            alert('Please fill out segment value fields');
            return false;
        }
    }
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