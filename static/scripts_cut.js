function noslicesize() {
    if ($("#overallCutValue").val() == '') {
        var numEmptyCutValues = $(".slicingValue").filter(function(){ return this.value == '' }).length
        if ( numEmptyCutValues > 1 ) {
            alert('Please enter a value for slice size or number of slices.');
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
        var slicinglabel = $(this).parents('.sliceoptionswrapper').find('.slicingoptionlabel');
        slicinglabel.html(slicinglabel.html().replace('Number of Slices', 'Slice Size'));

        var lastproportiondiv = $(this).parents('.sliceoptionswrapper').find('.lastproptableslot');
        lastproportiondiv.fadeIn(timeToToggle);
        lastproportiondiv.find('.lastpropinput').prop('disabled', false);
    });


    $(".numberradio").click( function() {
        var lastproportiondiv = $(this).parents('.sliceoptionswrapper').find('.lastproptableslot');
        lastproportiondiv.fadeOut(timeToToggle, function() {
            var slicinglabel = $(this).parents('.sliceoptionswrapper').find('.slicingoptionlabel');
            slicinglabel.html(slicinglabel.html().replace('Slice Size', 'Number of Slices'));
        });
        lastproportiondiv.find('.lastpropinput').prop('disabled', false);
    });


// = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    $(".indivcutbuttons").click( function() {
        var toggleDiv = $(this).parents('.individualpreviewwrapper').find('.sliceoptionswrapper');
        toggleDiv.slideToggle(timeToToggle);
    });

});