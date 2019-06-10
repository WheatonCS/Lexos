$(function(){

    // Initialize the "Color" button
    initialize_color_button(get_word_cloud_data);

    // Send the request for the word cloud data
    get_word_cloud_data();

    // If the "Generate" button is pressed, recreate the word cloud
    $("#generate-button").click(function(){
        get_word_cloud_data();
    })
});


/**
 * Requests the data for the word cloud and creates the word cloud.
 */
function get_word_cloud_data(){

    // Validate the "Term Count" input
    if(!validate_visualize_inputs()) return;

    // Remove any existing error messages
    remove_errors();

    // Display the loading overlay and disable the "PNG", "SVG" and "Generate"
    // buttons
    start_loading("#word-cloud-container",
        "#png-button, #svg-button, #generate-button");

    // Send a request for a list of the most frequent words and their number
    // of occurrences
    $.ajax({
        type: "POST",
        url: "word-cloud/get-word-counts",
        contentType: "application/JSON",
        data: JSON.stringify({maximum_top_words: $("#term-count-input").val()})
    })

        // If the request is successful, create the word cloud
        .done(create_word_cloud_layout)

        // If the request failed, display an error message, display
        // "Loading Failed" text, and enable the "Generate" button
        .fail(function(){
            error("Failed to retrieve the word cloud data.");
            add_text_overlay("#word-cloud-container", "Loading Failed");
            enable("#generate-button");
        });
}


/**
 * Creates the word cloud layout.
 * @param {string} response: The response from the get-word-counts request.
 */
let width;
let height;
let layout;
function create_word_cloud_layout(response){

    // Parse the JSON response
    response = parse_json(response);

    // If there are no active documents, display "No Active Documents" text
    // and return
    if(!response.length){
        add_text_overlay("#word-cloud-container", "No Active Documents");
        return;
    }

    // Otherwise, get the word cloud container element's width and height
    let word_cloud_container_element = $("#word-cloud-container");
    width = word_cloud_container_element.width();
    height = word_cloud_container_element.height();

    // Create a dataset of words and the size they should be
    let dataset = [];
    let base_size = 30;
    let maximum_size = Math.min(width, height)/3-base_size;
    for(const word of response)
        dataset.push({"text": word[0], "count": word[1],
            "normalized_count": word[2],
            "size": word[2]*maximum_size+base_size});

    // Initialize the word cloud layout
    layout = d3.layout.cloud()
        .size([width, height])
        .words(dataset)
        .padding(5)
        .rotate(function(){ return ~~(Math.random()*2)*90; })
        .font($("#font-input").val())
        .fontSize(function(d){ return d.size; })
        .on("end", create_word_cloud);

    // Create the word cloud layout
    layout.start();
}

/**
 * Creates the word cloud.
 * @param {string[]} dataset: The dataset of words and their sizes.
 */
function create_word_cloud(dataset){

    // Create the word cloud
    $(`<div id="word-cloud" class="hidden"></div>`)
        .appendTo("#word-cloud-container");

    d3.select("#word-cloud")

        .append("svg")
            .attr("width", layout.size()[0])
            .attr("height", layout.size()[1])

        .append("g")
            .attr("transform", "translate("+layout.size()[0]/2+
                ","+layout.size()[1]/2+")")
            .selectAll("text")
            .data(dataset)
            .enter()

        .append("text")
            .style("font-size", function(d){ return d.size+"px"; })
            .style("fill", function(d){
                return get_visualize_color(d.normalized_count);
            })
            .style("font-family", layout.font())
            .attr("text-anchor", "middle")
            .attr("transform", function(d){
                return "translate("+[d.x, d.y]+")rotate("+d.rotate+")";
            })
            .text(function(d){ return d.text; })

        .append("svg:title")
            .text(function(d){ return `Word: ${d.text} \nCount: ${d.count}`; });

    // Remove the loading overlay and fade the word cloud in
    finish_loading("#word-cloud-container", "#word-cloud",
        "#png-button, #svg-button, #generate-button");

    // Initialize the SVG and PNG download buttons
    initialize_png_link("svg", "#png-button", width, height, "word-cloud.png");
    initialize_svg_link("svg", "#svg-button", "word-cloud.svg");
}
