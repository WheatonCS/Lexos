$(function(){

    // If the "Upload" button was clicked...
    $("#dictionaries-section #upload-button").click(function(){

        // Click the file input element
        let file_input_element = $(`#file-input`);
        file_input_element.click();
    });
});
