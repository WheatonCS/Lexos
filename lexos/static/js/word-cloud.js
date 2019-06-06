let layout;
let color_map;

$(function(){

    // Display the loading overlay
    start_loading("#word-cloud-container");

    // Create the color map
    color_map = d3.scale.linear()
        .domain([100, 0])
        .range(["#505050", "#47BCFF"]);

    // Send a request for a list of the most frequent words and their number
    // of occurrences
    $.ajax({type: "GET", url: "word-cloud/get-word-counts"})

        // If the request is successful, create the word cloud
        .done(create_word_cloud_layout)
});


/**
 * Creates the word cloud layout.
 * @param {string} response: The response from the get-word-counts request.
 */
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
    let width = word_cloud_container_element.width();
    let height = word_cloud_container_element.height();

    // Create a dataset of words and the size they should be
    let dataset = [];
    let base_size = 30;
    let maximum_size = Math.min(width, height)/3-base_size;
    for(const word of response)
        dataset.push({"text": word[0], "count": word[1],
            "size": word[2]*maximum_size+base_size});

    // Initialize the word cloud layout
    layout = d3.layout.cloud()
        .size([width, height])
        .words(dataset)
        .padding(5)
        .rotate(function(){ return ~~(Math.random()*2)*90; })
        .font("Open Sans")
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
            .style("fill", function(d, i){ return color_map(i); })
            .style("font-family", layout.font())
            .attr("text-anchor", "middle")
            .attr("transform", function(d){
                return "translate("+[d.x, d.y]+")rotate("+d.rotate+")";
            })
            .text(function(d){ return d.text; })

        .append("svg:title")
            .text(function(d){ return `Word: ${d.text} \nCount: ${d.count}`; });

    // Remove the loading overlay and fade the word cloud in
    finish_loading("#word-cloud-container", "#word-cloud");
}
