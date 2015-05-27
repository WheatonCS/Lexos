$(function() {
	// Drag select needs to trigger behaviour in docManager (updating, checkbox, and de-selection) before it's ready for prime time.	
//	$('#docManager').selectable({
//	filter: 'tr',
//	stop: function(){
//		$("selected", this).each(function(){
//			var index = $("#docManager tr").index(this) - 1;
//			$('#docManager tbody tr:eq('+index+')').toggleClass('selected');
//			$('#docManager tbody tr:eq('+index+')').toggleClass('selected');
//		});
//		}
//	});
	
	$(".select-preview-text").click(function() {
		var id = $(this).parent('.select-preview-wrapper').prop('id');
		var that = $(this);

		// toggles active class on select page
		$.ajax({
			type: "POST",
			url: document.URL,
			data: id.toString(),
			contentType: 'charset=UTF-8',
			headers: { 'toggleFile': 'dummy' },
			success: function() {
				that.parent('.select-preview-wrapper').toggleClass('enabled');
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	$(".select-preview-filename").each(function() {
		$(this).prop('contenteditable', 'true');
	});

	$('.select-preview-filename').keydown(function(event) {
		var keyCode = event.which;

		if (keyCode == 13) { // "Enter"
			var contents = $(this).text();
			var id = $(this).parent().prop('id');
			var that = $(this);

			// toggles active class on select page
			$.ajax({
				type: "POST",
				url: document.URL,
				data: id.toString(),
				contentType: 'charset=UTF-8',
				headers: { 'setLabel': unescape(encodeURIComponent(contents.toString())) },
				success: function() {
					$('#error-message').css('color', 'green')
						.text("Label set: " + contents.toString())
						.show().fadeOut(2500);

					that.blur(); // Unfocus the field
				},
				error: function(jqXHR, textStatus, errorThrown){
					// display error if one
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});

			event.preventDefault();
		}
	});


	$("#disableall").click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: $(this).prop('id'),
			headers: { 'disableAll': 'dummy' },
			success: function() {
				$(".select-preview-wrapper").each(function() {
					$(this).removeClass("enabled");
				});
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	$("#selectall").click(function() {
		$.ajax({
			type: "POST",
			url: document.URL,
			data: $(this).prop('id'),
			headers: { 'selectAll': 'dummy' },
			success: function() {
				$(".select-preview-wrapper").each(function() {
					$(this).addClass("enabled");
				});
			},
			error: function(jqXHR, textStatus, errorThrown){
				// display error if one
				console.log("bad: " + textStatus + ": " + errorThrown);
			}
		});
	});

	// ajax call to send tag metadata on click
	$("#tagsubmit").click(function() {
		if ($("#tagfield").val()){
			// lowercases the tag. Can change to upper or whichever
			var classLabelToApply = $("#tagfield").val();

			// ajax call to send tag to backend
			$.ajax({
				type: "POST",
				url: document.URL,
				data: classLabelToApply,
				contentType: 'charset=UTF-8',
				headers: { 'applyClassLabel': 'dummy' },
				success: function() {
					// have visual feedback showing tag was applied
					$('.enabled').each(function() {
						$(this).children(".select-preview-label").html(classLabelToApply);
					});
				},
				error: function(jqXHR, textStatus, errorThrown){
					// display error if one exists
					console.log("bad: " + textStatus + ": " + errorThrown);
				}
			});
		}
	});

	// center the caution prompt in the window
	$('#delete-confirm-wrapper').center();

	$("#delete").click(function() {
		var enabled = $(".enabled");

		// if there are selected files
		if (enabled.length > 0) {
			// show the prompt
			$('#delete-confirm-wrapper').addClass("showing");
		}
	});
			
	// if they click cancel button, do nothing (just disappear)
	$('#cancel-bttn').click(function() {
		$('#delete-confirm-wrapper').removeClass("showing");
	});

	// if click confirm, delete the selection
	$('#confirm-delete-bttn').click(function() {
		var enabled = $(".enabled");
		
		$.ajax({
			type: "POST",
			url: document.URL,
			data: "",
			headers: { 'deleteActive': 'dummy' },
			success: function() {
				$('#delete-confirm-wrapper').removeClass("showing");
				enabled.remove();
			},
			error: function(jqXHR, textStatus, errorThrown){
				console.log(errorThrown);
			}
		});
	});
});

$(function() {
                
        // Initialise the docManager with the Ctrl Click Functionality as the Default
        var docManager = $('#docManager tbody').finderSelect({enableDesktopCtrlDefault:true});

        // Add a hook to the highlight function so that checkboxes in the selection are also checked.
        docManager.finderSelect('addHook','highlight:before', function(el) {
            el.find('input').prop('checked', true);
        });

        // Add a hook to the unHighlight function so that checkboxes in the selection are also unchecked.
        docManager.finderSelect('addHook','unHighlight:before', function(el) {
            el.find('input').prop('checked', false);
        });

        // Enable Double Click Event.
        docManager.finderSelect("children").dblclick(function() {
            alert( "Double Click detected. Useful for linking to detail page." );
        });

        // Prevent Checkboxes from being triggered twice when click on directly.
        docManager.on("click", ":checkbox", function(e){
            e.preventDefault();
        });

        // Add Select All functionality to the checkbox in the table header row.
        $('#docManager').find("thead input[type='checkbox']").change(function () {
            if ($(this).is(':checked')) {
                docManager.finderSelect('highlightAll');
            } else {
                docManager.finderSelect('unHighlightAll');

            }
        });

/* The code below has to be implemented through the 
context menu. */		
/*	var demo1 = $('#docManager').finderSelect({children:"tr",totalSelector:".demo1-count",menuSelector:"#demo1-menu"});

    $(".demo1-trash").click(function(){
        demo1.finderSelect("selected").remove();
        demo1.finderSelect("update");
    });

    $(".demo1-edit").click(function(){
        demo1.finderSelect("selected").each(function(){
          OpenInNewTab('http://pixlr.com/editor/?image='+$(this).attr('data-url'));
        });
    });*/
});

/* Context Menu */
/* https://github.com/mar10/jquery-ui-contextmenu */	
$(function(){
	/* Initialise by passing an array of entries. */
	$(document).contextmenu({
		delegate: ".hasmenu",
		preventContextMenuForPopup: true,
		preventSelect: true,
		taphold: true,
		menu: [
			{title: "Edit", cmd: "edit", uiIcon: "ui-icon-pencil"},
			{title: "Remove", cmd: "remove", uiIcon: "ui-icon-trash"},
			{title: "Remove All", cmd: "remove-all", uiIcon: "ui-icon-trash" }
			],
		// Handle menu selection 
		select: function(event, ui) {
			var $target = ui.target;
			switch(ui.cmd){
			case "edit":
				// Do something...
				break
			case "remove":
				// Do something...
				break
			case "remove-all":
				// Do something...
				break
			}
			//alert("You selected " + ui.cmd + " on \"" + $target.text()+"\".");
			// Optionally return false, to prevent closing the menu now
		},
		// Implement the beforeOpen callback to dynamically change the entries
		beforeOpen: function(event, ui) {
			var $menu = ui.menu,
				$target = ui.target,
				extraData = ui.extraData; // passed when menu was opened by call to open()

			// console.log("beforeOpen", event, ui, event.originalEvent.type);

			ui.menu.zIndex( $(event.target).zIndex() + 1);

			if ($('#docManager').finderSelect('selected').length < 2) {
				$(document).contextmenu("showEntry", "remove", true);
				$(document).contextmenu("showEntry", "remove-all", false);
			}
			else {
				$(document).contextmenu("showEntry", "remove", false);
				$(document).contextmenu("showEntry", "remove-all", true);			
			}
			// Optionally return false, to prevent opening the menu now
		}
	});

	/* Open and close an existing menu without programatically. */

	$("#triggerPopup").click(function(){
		// Trigger popup menu on the first target element
		$(document).contextmenu("open", $(".hasmenu:first"), {foo: "bar"});
		setTimeout(function(){
			$(document).contextmenu("close");
		}, 2000);
	});
});
