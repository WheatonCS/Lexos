function noslicesize() {
    if (document.getElementById('slicesize').value == '' && document.getElementById('slicenumber').value == '')
    {
        alert('Please enter a slice size or a number of slices.')
        return false;
    }
}

$(function () {
    $("#sizeradio").click( function() {
        document.getElementById("slicesize").disabled = false;
        document.getElementById("slicenumber").disabled = true;
        document.getElementById("lastprop").disabled = false;
        document.getElementById("lastprop").value = '50'
    });
    $("#numberradio").click( function() {
        document.getElementById("slicesize").disabled = true;
        document.getElementById("slicenumber").disabled = false;
        document.getElementById("lastprop").disabled = true;
        document.getElementById("lastprop").value = ''
    });

// = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    $(".indivcutbuttons").click( function() {
        // 1st parent = table column, 2nd parent = table row, sibling is other row, 1st child = table column, 2nd child is toggleDiv
        var toggleDiv = $(this).parent().parent().siblings().children().children();
        
        var timeToToggle = 250;
        toggleDiv.slideToggle(timeToToggle);
    });


});




// function hidechunkoption(num) {

//     switch(num)
//     {
//     	case 1:
//     		var show = document.getElementById("chunksize");
//     		var hide = document.getElementById("chunknumber");
//     		break;
//     	case 2:
//     		var hide = document.getElementById("chunksize");
//     		var show = document.getElementById("chunknumber");
//     		break;
//     }
//     hide.disabled = true;
//     hide.value = "";
//     show.disabled = false;

//     var proportion = document.getElementById("lastprop");
//     proportion.disabled ? (proportion.disabled = false, proportion.value = '50') : (proportion.disabled = true, proportion.value = '');
// }

