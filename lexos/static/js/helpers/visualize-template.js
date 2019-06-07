/**
 * Initialize the "Color" button.
 * @param {function} callback: The function to call when the popup's "Ok"
 *      button is clicked.
 */
function initialize_color_button(callback){

    // If the "Color" button is clicked, create a popup with the color options
    $("#color-button").click(function(){

        create_radio_options_popup("Color", "color", "#color-button",
            "#color-input", [
                ["lexos", "Lexos"],
                ["grey", "Grey"],
                ["emerald", "Emerald"],
                ["plum", "Plum"],
                ["ice", "Ice"],
                ["cherry-tree", "Cherry Tree"],
                ["ocean", "Ocean"]
            ]);

        // Call the callback when the "Ok" button is clicked
        $("#ok-button").click(callback);
    });
}

/**
 * Returns the interpolated color from the set color scheme.
 * @param {number} x: The interpolation value (0 to 1).
 * @returns {*}: The color.
 */
function get_visualize_color(x){
    let color_scheme = $("#color-button").text();
    x = Math.sqrt(x);

    switch(color_scheme){
        case "Lexos": return d3.scaleLinear()
            .domain([0, 1]).range(["#F3F3F3", "#47BCFF"])(x);
        case "Grey": return d3.interpolateGreys(x);
        case "Emerald": return d3.interpolateBuGn(x);
        case "Plum": return d3.interpolateBuPu(x);
        case "Ocean": return d3.interpolateGnBu(x);
        case "Ice": return d3.interpolatePuBu(x);
        case "Cherry Tree": return d3.interpolatePuRd(x);
    }
}


/**
 * Generates an SVG document from an SVG element
 * @param {string} svg_query: The query for the SVG element.
 * @returns {string}: The SVG document data.
 */
function generate_svg_data(svg_query){
    let svg_document_type = document.implementation.createDocumentType(
        "svg",  "-//W3C//DTD SVG 1.1//EN",
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd");

    let svg_document = document.implementation.createDocument(
        "http://www.w3.org/2000/svg", "svg", svg_document_type);

    svg_document.replaceChild($(svg_query)[0].cloneNode(true),
        svg_document.documentElement);

    return (new XMLSerializer()).serializeToString(svg_document);
}


/**
 * Creates a SVG download link for an SVG element.
 * @param {string} svg_query: The query for the SVG element.
 * @param {string} link_query: The query for the link element to populate with
 *      the generated SVG data.
 * @param {string} download_name: The name of the file to send as a download.
 */
function initialize_svg_link(svg_query, link_query, download_name){

    // Assign the link the SVG data
    let svg_link_element = $(link_query);
    svg_link_element.attr("download", download_name);
    svg_link_element.attr("href", "data:image/svg+xml; charset=utf8, "+
        encodeURIComponent(generate_svg_data(svg_query)));
}


/**
 * Create a PNG download link for an SVG element.
 * @param {string} svg_query: The query for the SVG element.
 * @param {string} link_query: The query for the link element to populate with
 *      the generated PNG data.
 * @param {number} width: The width of the PNG.
 * @param {number} height: The height of the PNG.
 * @param {string} download_name: The name of the file to send as a download.
 */
function initialize_png_link(svg_query,
    link_query, width, height, download_name){

    let canvas = document.createElement("canvas");
    let context = canvas.getContext("2d");

    canvas.width = width;
    canvas.height = height;

    let image = new Image();

    image.onload = function(){

        context.clearRect(0, 0, width, height);
        context.drawImage(image, 0, 0, width, height);

        let png_link_element = $(link_query);
        png_link_element.attr("download", download_name);
        png_link_element.attr("href", canvas.toDataURL());
    };

    image.src = "data:image/svg+xml; charset=utf8, "+
        encodeURIComponent(generate_svg_data(svg_query));
}


/**
 * Validate the visualize inputs.
 */
function validate_visualize_inputs(){

    // "Term Count"
    if(!validate_number($("#term-count-input").val(), 1, 1000)){
        error("Invalid term count.");
        return false;
    }

    return true;
}
