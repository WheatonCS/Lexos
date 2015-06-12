$(function() {
	// Disable dtm toggle when matrix
	if (matrixExist === 0){
		$(".toggle-dtm").unbind("click")
						.css("background-color", "gray");
	}
	
	var totalGroups = 2, groupID;

	// Add one more segment group when add button clicked
	$("#addOneGroup").click(function() {

		// Record selected file names
		var selected = [];
		$("#group-2 input:checked").each(function() {
		    selected.push($(this).attr('name'));
		});

		for(var i=0; i<selected.length;i++){
			$("#"+selected[i]).removeAttr('checked');
		}

		// Add new cloned group to the list and assign an 
		var $block = $("#group-2");
		var $clone = $block.clone();
		$clone.appendTo("#addGroups");
		totalGroups++;
		groupID = "group-" + String(totalGroups);

		// Update the total number of groups
		var newGroup = $("#addGroups :last-child");
		newGroup.attr("id", groupID);
		$("#addGroups :last-child :nth-child(2)").contents().first().replaceWith("Group "+String(totalGroups));

	});

	// Delete one segment group when minus button clicked
	$("#deleteOneGroup").click(function() {
		if (totalGroups > 2) {

			var newLastGroup = document.getElementById("group-" + String(totalGroups-1));
			newLastGroup.nextElementSibling.remove();

			totalGroups--;
		}
	});

	// $("#gettopword").attr('disabled', 'true');

	function updateTokenizeCheckbox() {
		$('input[type=radio][name=normalizeType]').attr('disabled', 'true');
		$('input[type=radio][name=normalizeType]').parent('label').addClass('disabled');
	}

	updateTokenizeCheckbox();

});
