let checked_options = {
    "distance-metric": "euclidean",
    "linkage-method": "average",
    "orientation": "bottom"
};

$(function(){
    // Register distance metric button callback
    $("#distance-metric-button").click(function(){
        create_options_popup("distance-metric", [
            ["euclidean", "Euclidean"],
            ["minkowski", "Minkowski"],
            ["manhattan", "Manhattan"],
            ["standardized euclidean", "Standardized Euclidean"],
            ["squared euclidean", "Squared Euclidean"],
            ["cosine", "Cosine"],
            ["correlation", "Correlation"],
            ["hamming", "Hamming"],
            ["chebychev", "Chebychev"],
            ["jaccard", "Jaccard"],
            ["canberra", "Canberra"],
            ["braycurtis", "Braycurtis"],
        ]);
    });

    // Register linkage method button callback
    $("#linkage-method-button").click(function(){
        create_options_popup("linkage-method", [
            ["average", "Average"],
            ["single", "Single"],
            ["complete", "Complete"],
            ["weighted", "Weighted"]
        ]);
    });

    // Register orientation button callback
    $("#orientation-button").click(function(){
        create_options_popup("orientation-text", [
            ["bottom", "Bottom"],
            ["top", "Top"]
        ]);
    });

    $.ajax({type: "GET", url: "/active-file-ids"}).done(initialize);
});


function initialize(response){

    // Initialize legacy inputs
    if(!initialize_legacy_inputs(response)) return;

    // Create the dendrogram
    send_ajax_form_request("dendrogram/graph").done(function(response){
        console.log(response);
        $("#dendrogram").html(response);
    });
}


/**
 * Creates a popup of radio buttons.
 * @param name: The name of the options group.
 * @param checked_option: The value of the option to check.
 * @param options
 */
function create_options_popup(name, options){

    // Create the popup
    create_popup();
    let popup_content = $("#popup-content");

    for(const option of options) {
        let element = $(`
            <div>
                <label class="circle-label">
                    <input type="radio" name="${name}-input" value="${option[0]}">
                    <span>${option[1]}</span>
                </label>
            </div>
        `).appendTo(popup_content);

        if(option[0] == checked_options[name]){
            console.log(option[0], checked_options[name]);
            element.find(`#${name}-input`).prop("checked", true);
        }
    }

    $(`<h3 id="ok-button" class="selectable">OK</h3>`).appendTo(popup_content);

    // Create "OK" button callback
    $("#ok-button").click(function(){
        let selected_element = $(`input[name="${name}"]:checked`);
        $(`#${name}-input`).val(selected_element.val());
        $(`#${name}-text`).text(selected_element.closest("div").find("span").html());
        checked_options[name] = selected_element.val();
        close_popup();
    });
}
