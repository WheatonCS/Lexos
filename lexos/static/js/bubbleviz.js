$(function(){

    // Display the loading overlay
    start_loading("#bubbleviz");

    // Create the bubbleviz
    $.ajax({type: "GET", url: "bubbleviz/get-word-counts"})
        .done(create_bubbleviz);
});

/**
 * Create the bubbleviz.
 * @param {string} response: The response from the "bubbleviz/get-word-counts"
 *      request.
 */
function create_bubbleviz(response){

    let word_counts = parse_json(response);

    // If there are no word counts, display "No Active Documents" text and
    // return
    if(!word_counts.length){
        add_text_overlay("form", "No Active Documents");
        return;
    }

    // Parse the response for the dataset of word counts
    let dataset = {children: word_counts};

    // Set the diameter of the bubbleviz graph as the minimum axis of the
    // bubbleviz element
    let bubbleviz_element = $("#bubbleviz");
    let diameter = Math.min(bubbleviz_element.width(),
        bubbleviz_element.height());

    let base_font_size = 5;

    // Create the color map
    let color = d3.scaleLinear()
        .domain([0, 1])
        .range(["#505050", "#47BCFF"]);

    // Create the bubbleviz
    let bubble = d3.pack(dataset)
        .size([diameter, diameter])
        .padding(3);

    let svg = d3.select("#bubbleviz")
        .append("svg")
            .style("width", diameter+"px")
            .style("height", diameter+"px")
            .attr("class", "bubble");

    let nodes = d3.hierarchy(dataset)
        .sum(function(d){ return d.value; });

    let node = svg.selectAll(".node")
        .data(bubble(nodes).descendants())
        .enter()
        .filter(function(d){ return !d.children; })
        .append("g")
            .attr("class", "node")
            .attr("transform", function(d){ return "translate("+d.x+", "+d.y+')'; });

    node.append("circle")
        .attr("r", function(d){ return d.r; })
        .style("fill", function(d, i){ return color(d.data.value); });

    node.append("text")
        .attr("dy", ".2em")
        .style("text-anchor", "middle")
        .text(function(d){ return d.data.word; })
        .attr("font-family", "Open Sans")
        .attr("font-size", function(d){ return d.r/3+base_font_size; })
        .attr("fill", "#E3E3E3")

    node.append("svg:title")
        .text(function(d){ return "Word: "+d.data.word+"\nCount: "+d.data.count; });

    // Fade in the bubbleviz
    d3.select(self.frameElement).style("height", diameter+"px");
    finish_loading("#bubbleviz", "#bubbleviz");
}
