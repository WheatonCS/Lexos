function noslicesize() {
    if (document.getElementById('slicefield').value == '')
    {
        alert('Please enter a value for slice size or number of slices.');
        return false;
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
    var timeToToggle = 350;
    $(".sizeradio").click( function() {
        var slicinglabel = $(this).parents('.sliceoptionswrapper').find('.slicingoptionlabel');
        slicinglabel.text('Slice Size:');

        var lastproportiondiv = $(this).parents('.sliceoptionswrapper').find('.lastproptableslot');
        lastproportiondiv.slideDown(timeToToggle);
        lastproportiondiv.find('.lastpropinput').prop('disabled', false);
    });


    $(".numberradio").click( function() {
        var slicinglabel = $(this).parents('.sliceoptionswrapper').find('.slicingoptionlabel');
        slicinglabel.text('Number of Slices:');

        var lastproportiondiv = $(this).parents('.sliceoptionswrapper').find('.lastproptableslot');
        lastproportiondiv.slideUp(timeToToggle);
        lastproportiondiv.find('.lastpropinput').prop('disabled', true);
    });


// = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    $(".indivcutbuttons").click( function() {
        // 1st parent = table column, 2nd parent = table row, sibling is other row, 1st child = table column, 2nd child is toggleDiv
        var toggleDiv = $(this).parents('.individualpreview').find('.sliceoptionswrapper');
        
        toggleDiv.slideToggle(timeToToggle);
    });

});