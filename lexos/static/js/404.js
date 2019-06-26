$(function() {
    window.addEventListener ('load', OnLoad, true);
    window.addEventListener ('resize', OnResize, true);
});

/**
 * Re-sizes the document to fit the canvas
 */
function OnResize(){
    var canvas = document.getElementById ('fullscreen');
    canvas.width = document.body.clientWidth;
    canvas.height = document.body.clientHeight;
}

/**
 *
 */
function OnLoad(){
    OnResize();
    LoadOnline3DModels();
}
