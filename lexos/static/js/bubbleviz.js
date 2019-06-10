$(function(){

    // Initialize the "Color" button
    initialize_color_button();

    // Create the bubbleviz
    send_word_counts_request();

    // If the "Generate" button is pressed, recreate the bubbleviz
    $("#generate-button").click(send_word_counts_request);
});


/**
 * Sends the request for the word counts and creates the bubbleviz.
 */
function send_word_counts_request(){

    // Validate the "Term Count" input
    if(!validate_visualize_inputs()) return;

    // Display the loading overlay and disable the "PNG", "SVG" and "Generate"
    // buttons
    start_loading("#bubbleviz", "#png-button, #svg-button, #generate-button");

    // Send the request for the word counts
    $.ajax({
        type: "POST",
        url: "bubbleviz/get-word-counts",
        contentType: "application/JSON",
        data: JSON.stringify({maximum_top_words: $("#term-count-input").val()})
    })

    // If the request is successful, create the bubbleviz
    .done(create_bubbleviz)

    // If the request failed, display and error
    .fail(function(){ error("Failed to retrieve the bubbleviz data."); });
}


/**
 * Create the bubbleviz.
 * @param {string} response: The response from the "bubbleviz/get-word-counts"
 *      request.
 */
function create_bubbleviz(response){
    // Define the div for the tooltip
    var tooltip = d3.select("body").append("div")
        .attr("class", "d3 tooltip")
        .style("opacity", 0);
    d3.select('.d3tooltip').attr('role', 'tooltip')

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

    // Create the bubbleviz
    let bubble = d3.pack(dataset)
        .size([diameter, diameter])
        .padding(3);

    let svg = d3.select("#bubbleviz")
        .append("svg")
            .attr("version", "1.1")
            .attr("xmlns", "http://www.w3.org/2000/svg")

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
            .attr("transform", function(d){
                return "translate("+d.x+", "+d.y+')';
            });

    node.append("circle")
        .attr("r", function(d){ return d.r; })
        .style("fill", function(d){
            return get_visualize_color(d.data.value);
        })
        .on("mouseover", function () {
            d3.select(this.parentNode.childNodes[0]).style('fill', 'gold')
            tooltip.style("opacity", 1);
            // tooltip.transition()
            //     .duration(20)
            //     .style("opacity", .9);
            //tooltip.html(`<div class="tooltip-arrow"></div><div class="tooltip-inner"> Word: ${d.data.word}<br>Count: ${d.data.count}</div>`);
        })
        .on("mousemove", function (d){
            tooltip
                .text(`Word: ${d.data.word}\nCount: ${d.data.count}`)
                .style('left', (d3.event.pageX + 34) + 'px')
                .style('top', (d3.event.pageY - 12) + 'px');
        })
        .on("mouseout", function () {
            d3.select(this.parentNode.childNodes[0]).style("fill", function(d){ return get_visualize_color(d.data.value)})
            //tooltip.transition()
                //.duration(20)
            tooltip.style("opacity", 0);
        });

    node.append("text")
        .attr("dy", ".3em")
        .style("text-anchor", "middle")
        .text(function(d){ return d.data.word; })
        .attr("font-family", $("#font-input").val())
        .attr("font-size", function(d){ return d.r/(d.data.word.length/3); })
        .attr("fill", "#FFFFFF")
        .on("mouseover", function () {
            d3.select(this.parentNode.childNodes[0]).style('fill', 'gold')
            tooltip.style("opacity", 1);
            // tooltip.transition()
            //     .duration(20)
            //     .style("opacity", .9);
            // tooltip.html(`<div class="tooltip-arrow"></div><div class="tooltip-inner"> Word: ${d.data.word}<br>Count: ${d.data.count}</div>`);
        })
        .on("mousemove", function (d){
            tooltip
                .text(`Word: ${d.data.word}\nCount: ${d.data.count}`)
                .style('left', (d3.event.pageX + 34) + 'px')
                .style('top', (d3.event.pageY - 12) + 'px');
        })
        .on("mouseout", function () {
            d3.select(this.parentNode.childNodes[0]).style("fill", function(d){ return get_visualize_color(d.data.value)})
            //tooltip.transition()
                //.duration(20)
            tooltip.style("opacity", 0);
        });

    // node.append("svg:title")
    //     .text(function(d){ return "Word: "+d.data.word+"\nCount: "+d.data.count; });

    // Fade in the bubbleviz
    d3.select(self.frameElement).style("height", diameter+"px");
    finish_loading("#bubbleviz", "#bubbleviz",
        "#png-button, #svg-button, #generate-button");

    // Initialize the SVG and PNG download buttons
    initialize_png_link("svg", "#png-button", diameter, diameter, "bubbleviz.png");
    initialize_svg_link("svg", "#svg-button", "bubbleviz.svg");
}
