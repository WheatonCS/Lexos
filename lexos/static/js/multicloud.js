let layouts = [];
let color;

$(function(){

    // Display the loading overlay
    add_loading_overlay("#multicloud");

    // Create the color map
    color = d3.scale.linear()
        .domain([100, 0])
        .range(["#505050", "#47BCFF"]);

    // Create the multicloud
    $.ajax({type: "GET", url: "multicloud/get-word-counts"})
        .done(create_word_cloud_layouts);
});


/**
 * Creates the multicloud (a word cloud for each active document).
 * @param {jqXHR} response: The response from the get-word-counts request.
 */
function create_word_cloud_layouts(response){

    // Parse the JSON response
    response = $.parseJSON(response);

    // Clear any existing content in the multicloud element
    let multicloud_element = $("#multicloud");
    multicloud_element.empty();

    // If there are no active documents, display "No Active Documents" text
    // and return
    if(!response.length){
        add_text_overlay("No Active Documents");
        return;
    }

    // Otherwise, create a word cloud for each document
    for(let i = 0; i < response.length; ++i){

        // Get the document's data
        let document = response[i];

        // Create the word cloud element
        let word_cloud_element = $(`
            <div id="word-cloud-wrapper-${i}" class="word-cloud-wrapper">
                <h3 class="title">${document.name}</h3>
                <div id="word-cloud-${i}" class="word-cloud"></div>
            </div>
        `).appendTo(multicloud_element).find(".word-cloud");

        // Calculate the sizes
        let width = word_cloud_element.width();
        let height = word_cloud_element.height();
        let minimum_axis = Math.min(width, height);
        let base_size = minimum_axis/50;
        let maximum_size = minimum_axis/3-base_size;

        // Create the list of the words' text and sizes
        let words = []
        for(const word of document.words)
            words.push({"text": word[0], "size":
                word[1]*maximum_size+base_size});

        // Create the layout
        create_word_cloud_layout(i, document.name, words, width, height);
    }
}


/**
 * Creates a word cloud layout.
 *
 * @param {Number} id: The ID of the layout.
 * @param {String} name: The name of the document.
 * @param {Array} words: The top words in the document.
 * @param {Number} width: The width of the word cloud.
 * @param {Number} height: The height of the word cloud.
 */
function create_word_cloud_layout(id, name, words, width, height){

    // Create the word cloud layout
    layouts[id] = d3.layout.cloud()
        .size([width, height])
        .words(words)
        .padding(5)
        .rotate(function(){ return ~~(Math.random()*2)*90; })
        .font("Open Sans")
        .fontSize(function(d){ return d.size; })
        .on("end", function(words){
            create_word_cloud(id, name, words, width, height);
        });

    // Start the render
    layouts[id].start();
}


/**
 * Creates a word cloud.
 *
 * @param {Number} id: The ID of the layout.
 * @param {string} name: The name of the document.
 * @param {List} words: The words in the layout.
 * @param {Number} width: The width of the word cloud.
 * @param {Number} height: The height of the word cloud.
 */
function create_word_cloud(id, name, words, width, height){

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
            .style("fill", function(d, i){ return color(i); })
            .style("font-family", layout.font())
            .attr("text-anchor", "middle")
            .attr("transform", function(d){
                return "translate("+[d.x, d.y]+")rotate("+d.rotate+")";
            })
            .text(function(d){ return d.text; });

    // Fade the word cloud wrapper element in
    fade_in(`#word-cloud-wrapper-${id}`);
}
