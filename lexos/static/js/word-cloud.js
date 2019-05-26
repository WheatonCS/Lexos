let layout;
let color_map;

$(function(){

    // Create the color map
    color_map = d3.scale.linear()
        .domain([100, 0])
        .range(["#505050", "#47BCFF"]);

    // Create the word cloud layout
    $.ajax({type: "GET", url: "word-cloud/get-word-counts"})
        .done(create_word_cloud_layout)
});


/**
 * Creates the word cloud layout.
 *
 * @param {jqXHR} response: The response from the get-word-counts request.
 */
function create_word_cloud_layout(response){

    // Parse the JSON response
    response = $.parseJSON(response);

    // If there are no active documents, display "no active documents" text
    if(!response.length){
        $(`<h3>No Active Documents</h3>`).appendTo("#word-cloud");
        $("#word-cloud").css("opacity", "1");
        return;
    }

    // Get the word cloud element's width and height
    let word_cloud_element = $("#word-cloud");
    let width = word_cloud_element.width();
    let height = word_cloud_element.height();

    // Create the list of words
    let words = [];
    let base_size = 30;
    let maximum_size = Math.min(width, height)/3-base_size;
    for(const word of response){
        words.push({"text": word[0], "size": word[1]*maximum_size+base_size});
    }

    // Create the word cloud layout
    layout = d3.layout.cloud()
        .size([width, height])
        .words(words)
        .padding(5)
        .rotate(function(){ return ~~(Math.random()*2)*90; })
        .font("Open Sans")
        .fontSize(function(d){ return d.size; })
        .on("end", draw_word_cloud);

    // Start the render
    layout.start();
}

/**
 * Draws the word cloud.
 *
 * @param {List} words: The words in the layout.
 */
function draw_word_cloud(words){

    // Draw the word cloud
    d3.select("#word-cloud")
        .append("svg")
            .attr("width", layout.size()[0])
            .attr("height", layout.size()[1])
        .append("g")
            .attr("transform", "translate("+layout.size()[0]/2+","+layout.size()[1]/2+")")
            .selectAll("text")
            .data(words)
            .enter()
        .append("text")
            .style("font-size", function(d){ return d.size+"px"; })
            .style("fill", function(d, i){ return color_map(i); })
            .style("font-family", layout.font())
            .attr("text-anchor", "middle")
            .attr("transform", function(d){
                return "translate("+[d.x, d.y]+")rotate("+d.rotate+")";
            })
            .text(function(d){ return d.text; });

    // Fade the word cloud in
    $("#word-cloud").css("opacity", "1");
}
