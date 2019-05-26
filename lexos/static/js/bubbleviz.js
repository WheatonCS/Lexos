$(function(){

    // Create the bubbleviz
    $.ajax({type: "GET", url: "bubbleviz/get-word-counts"})
        .done(create_bubbleviz);
});

function create_bubbleviz(response){

    // Parse the response
    let dataset = {children: $.parseJSON(response)};

    // Get the width and height
    let bubbleviz_element = $("#bubbleviz");
    let width = bubbleviz_element.width();
    let height = bubbleviz_element.height();

    // Create the color map
    let color = d3.scaleLinear()
        .domain([0, 1])
        .range(["#505050", "#47BCFF"]);

    // Create the bubbleviz
    let bubble = d3.pack(dataset)
        .size([width, height])
        .padding(3);

    let svg = d3.select("#bubbleviz")
        .append("svg")
            .style("width", width)
            .style("height", height)
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
        .attr("font-size", function(d){ return d.r/5; })
        .attr("fill", "#E3E3E3");

    // Show the bubbleviz
    d3.select(self.frameElement).style("height", height+"px");
    bubbleviz_element.css("opacity", "1");
}
