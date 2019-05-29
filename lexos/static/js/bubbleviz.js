$(function(){

    // Display the loading overlay
    add_loading_overlay("#bubbleviz");

    // Create the bubbleviz
    $.ajax({type: "GET", url: "bubbleviz/get-word-counts"})
        .done(create_bubbleviz);
});

function create_bubbleviz(response){

    // Parse the response for the dataset of word counts
    let dataset = {children: $.parseJSON(response)};

    // Get the width and height of the bubbleviz element
    let bubbleviz_element = $("#bubbleviz");
    let diameter = Math.min(bubbleviz_element.width(),
        bubbleviz_element.height());
    let base_font_size = 5;

    // Create the color map
    let color = d3.scaleLinear()
        .domain([0, 1])
        .range(["#505050", "#47BCFF"]);

    // Clear any existing content
    bubbleviz_element.empty();

    // Create the bubbleviz
    let bubble = d3.pack(dataset)
        .size([diameter, diameter])
        .padding(3);

    let svg = d3.select("#bubbleviz")
        .append("svg")
            .style("width", diameter)
            .style("height", diameter)
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
        .text(function(d){ return d.data.name; })
        .attr("font-family", "Open Sans")
        .attr("font-size", function(d){ return d.r/3+base_font_size; })
        .attr("fill", "#E3E3E3");

    // Fade in the bubbleviz
    d3.select(self.frameElement).style("height", diameter+"px");
    fade_in("#bubbleviz");
}
