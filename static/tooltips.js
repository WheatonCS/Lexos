$(function() {
    $( document ).tooltip({
        position: {
            my: "left-25 bottom-12",
            at: "left top",
            using: function( position, feedback ) {
                $( this ).css( position );
                $( "<div>" )
                    .addClass( "arrow" )
                    .addClass( feedback.vertical )
                    .addClass( feedback.horizontal )
                    .appendTo( this );
            }
        }
    });
});