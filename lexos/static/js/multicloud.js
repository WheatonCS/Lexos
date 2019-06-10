let layouts = [];
let word_cloud_count;
let rendered_count;

$(function(){

    // Initialize the "Color" button
    initialize_color_button(get_multicloud_data);

    // Create the multicloud
    get_multicloud_data();

    // If the "Generate" button is pressed, recreate the multicloud
    $("#generate-button").click(get_multicloud_data);
});


/**
 * Get the multicloud data.
 */
function get_multicloud_data(){

    // Validate the "Term Count" input
    if(!validate_visualize_inputs()) return;

    // Remove any error messages
    remove_errors();

    // Reset the rendered word cloud count
    rendered_count = 0;

    // Display the loading overlay and disable the "PNG", "SVG" and "Generate"
    // buttons
    start_loading("#multicloud", "#png-button, #svg-button, #generate-button");

    // Send a request to get the word counts
    $.ajax({
        type: "POST",
        url: "multicloud/get-word-counts",
        contentType: "application/JSON",
        data: JSON.stringify({maximum_top_words: $("#term-count-input").val()})
    })

        // If the request was successful, create the multicloud
        .done(create_word_cloud_layouts)

        // If the request failed, display an error message, display
        // "Loading Failed" text, and enable the "Generate" button
        .fail(function(){
            error("Failed to retrieve the multicloud data.");
            add_text_overlay("#multicloud", "Loading Failed");
            enable("#generate-button");
        });
}


/**
 * Creates the multicloud (a word cloud for each active document).
 * @param {string} response: The response from the get-word-counts request.
 */
let diameter;
function create_word_cloud_layouts(response){

    // Parse the JSON response
    response = parse_json(response);

    // If there are no active documents, display "No Active Documents" text
    // and return
    word_cloud_count = response.length;
    if(!word_cloud_count){
        add_text_overlay("#multicloud", "No Active Documents");
        return;
    }

    // Otherwise, create a word cloud for each document
    for(let i = 0; i < word_cloud_count; ++i){

        // Get the document's data
        let document = response[i];

        // Create the word cloud element
        $(`
            <div id="word-cloud-wrapper-${i}" class="word-cloud-wrapper">
            
                <div class="vertical-splitter section-top">
                    <h3 class="title">${document.name}</h3>
                    
                    <div class="right-justified">
                        <a id="png-button-${i}" class="button">PNG</a>
                        <a id="svg-button-${i}" class="button">SVG</a>
                    </div>
                </div>
                
                <div id="word-cloud-${i}" class="word-cloud"></div>
            </div>
        `).appendTo("#multicloud").find(".word-cloud");

        // Calculate the sizes
        diameter = rem_to_px(46);
        let base_size = diameter/50;
        let maximum_size = diameter/3-base_size;

        // Create the list of the words' text and sizes
        let words = []
        for(const word of document.words)
            words.push({"text": word[0], "count": word[1],
                "normalized_count": word[2],
                "size": word[2]*maximum_size+base_size});

        // Create the layout
        create_word_cloud_layout(i, document.name, words, diameter);
    }
}


/**
 * Creates a word cloud layout.
 * @param {number} id: The ID of the layout.
 * @param {string} name: The name of the document.
 * @param {array} words: The top words in the document.
 * @param {number} diameter: The diameter of the word cloud.
 */
function create_word_cloud_layout(id, name, words, diameter){

    // Create the word cloud layout
    layouts[id] = d3.layout.cloud()
        .size([diameter, diameter])
        .words(words)
        .padding(5)
        .rotate(function(){ return ~~(Math.random()*2)*90; })
        .font($("#font-input").val())
        .fontSize(function(d){ return d.size; })
        .on("end", function(words){
            create_word_cloud(id, name, words);
        });

    // Start the render
    layouts[id].start();
}


/**
 * Creates a word cloud.
 * @param {number} id: The ID of the layout.
 * @param {string} name: The name of the document.
 * @param {list} words: The words in the layout.
 */
function create_word_cloud(id, name, words){

    let layout = layouts[id];

    // Create the word cloud
    d3.select(`#word-cloud-${id}`)

        .append("svg")
            .attr("width", layout.size()[0])
            .attr("height", layout.size()[1])

        .append("g")
            .attr("transform", "translate("+
                layout.size()[0]/2+","+layout.size()[1]/2+")")
            .selectAll("text")
            .data(words)
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

    // Initialize the PNG and SVG download buttons
    initialize_png_link(`#word-cloud-${id} svg`, `#png-button-${id}`,
        diameter, diameter, "multicloud.png");
    initialize_svg_link(`#word-cloud-${id} svg`,
        `#svg-button-${id}`, "multicloud.svg");

    // Remove the loading overlay and fade in the word clouds if this is the
    // last word cloud to render
    if(++rendered_count === word_cloud_count)
        finish_loading("#multicloud", ".word-cloud-wrapper",
            "#png-button, #svg-button, #generate-button");
}
