$(document).ready(function () {

    $('#hamburger').on('click', function(event){

    	togglePanel(event);
    });
    $('.slideout-menu-toggle').on('click', function(event){
    	togglePanel(event);
    });

    // http://alijafarian.com/jquery-horizontal-slideout-menu/
    function togglePanel(event) {
    	event.preventDefault();

    	// Create menu variables
    	var slideoutMenu = $('.slideout-menu');
    	var slideoutMenuWidth = $('.slideout-menu').width();
    	
    	// Toggle the open class
    	slideoutMenu.toggleClass("open");
    	
    	// Slide the panel
    	if (slideoutMenu.hasClass("open")) {
	    	slideoutMenu.animate({
		    	left: "0px"
	    	});	
    	} else {
	    	slideoutMenu.animate({
		    	left: -slideoutMenuWidth
	    	}, 250);
	    	$("#panel-content").remove();	
    	}
    }

	/* Triggering event with click on class ITMtrigger */
    $('.ITMtrigger').on('click', function(event){
        event.preventDefault();

        // Get the slug from the event
        if ($(this).attr("data-slug")) {
        	var slug = $(this).attr("data-slug");
        }
        // Or get it from the page title
        else {
			var slug = $("#titleprefix").attr("data-slug");
        }

        // Detect trigger type, panel, dialog, or video-dialog
        if ($(this).hasClass("panel")) {
            var type = "panel";
            var panelContent = $("#ITMpanelContent").empty();
            $("#panel-status").show();
        }
        else if ($(this).hasClass("video-dialog")) {
            var type = "video-dialog";
            var dialogContent = $("#ITMdialog").empty();
            $("#dialog-status").appendTo(dialogContent);
            $("#dialog-status").css("display", "block");
            $("#ITMdialog").dialog({
                title: "Loading title...",
                width: 450,
                height: 450,
            });
        }
        else {
            var type = "dialog";
            var dialogContent = $("#ITMdialogContent").empty();
            $("#dialog-status").appendTo(dialogContent);
            $("#dialog-status").css("display", "block");
            $("#ITMdialog").dialog({
                title: "Loading title...",
                width: 450,
                height: 450,
                close: function(){
                    $("#ITMdialog").empty();
                } 
            });
        }

        // Call the Scalar API
        callAPI(slug, type);
	});
});


/* Call Scalar API */
function callAPI(slug, type) {

	// No reason not to hard code this here since we only need the slug
	var url = "http://scalar.usc.edu/works/lexos/rdf/node/"+slug+"?rec=0&format=json";

	// Ajax call
	$.ajax({
        type:"GET",
        url:url,
        dataType:'jsonp',
//        beforeSend: function(data){
//		},
        // Pass the data and type to the handleSuccess function
        success: function(data){
    		processData(data, type, url);
		}, 
//        complete: function(){
//		},
        error: handleError
    });
}

/* Handle a failed API call. */
function handleError(XMLHttpRequest, textStatus, errorThrown) {
    $('#status').html(textstatus+'"<br>"'+errorThrown).show();
}
            
/* Process the data. */
function processData(data, type, url) {
	for (var nodeProp in data) {
        node = data[nodeProp]
        content_path = node['http://rdfs.org/sioc/ns#content'];
        if (node['http://purl.org/dc/terms/title'] != null) {
            var title = node['http://purl.org/dc/terms/title'][0].value;
        }
        if (node['http://simile.mit.edu/2003/10/ontologies/artstor#url'] != null) {
            var video_url = node['http://simile.mit.edu/2003/10/ontologies/artstor#url'][0].value;
            //var url = node['http://purl.org/dc/terms/isVersionOf'][0].value;
        }
        if (node['http://simile.mit.edu/2003/10/ontologies/artstor#url'] != null) {
            var url = node['http://purl.org/dc/terms/isVersionOf'][0].value;
        }
        if (content_path != null) {
        	var content = content_path[0].value;
        	content = content.replace(new RegExp('\r?\n\r?\n','g'), '<br><br>'); // Replace line breaks
        }
    }
    displayITMcontent(content, title, url, type, video_url);
}

/* Display the results. */
function displayITMcontent(content, title, url, type, video_url) {
	// Fork here based on type
	switch (type) {
		case "panel":
		titleLink = '<h3><a href="'+url+'" target="_blank">'+title+'</a></h3>';
		$(".slideout-menu").append('<div id="panel-content">'+titleLink+content+'</div>');
		$("#panel-status").hide();
		break;

		case "dialog":
        $("#ITMdialog").dialog('option', 'title', title);
		$("#ITMdialog").append(content);
        $("#dialog-status").hide();
        $("#dialog-status").appendTo($("#dialogStatusHolder"));
		break;

		// Works only with YouTube videos
		case "video-dialog":
		var youtube_url = video_url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/");
        $("#ITMdialog").dialog('option', 'title', title);
		$("#ITMdialog").append('<iframe height="99%" width="99%" src="'+youtube_url+'"></iframe>');
        $("#dialog-status").hide();
        $("#dialog-status").appendTo($("#dialogStatusHolder"));
		break;
	}
}