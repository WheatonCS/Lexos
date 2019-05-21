$("document").ready(function(){

    // Get initial active document document previews
    return $.ajax({
        type: "GET",
        url: "/scrub/get-document-previews",
    })
    .done(create_document_previews);
});


function create_document_previews(response){

    let document_previews = $("#previews");
    let previews = JSON.parse(response);

    for(const preview of previews){
        $(`
            <div class="preview">
                <h3 class="preview-name">${preview[2]}</h3>
                <h3 class="preview-text">${preview[3]}</h3>
            </div>
        `).appendTo(document_previews);
    }
}
