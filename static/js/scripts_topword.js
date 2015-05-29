$(function() {

	var totalGroups = 2, groupID;

	$("#addOneGroup").click(function() {
		var $block = $("#group-2");

		var selected = [];
		console.log($("#group-2 input:checked"));

		$("#group-2 input:checked").each(function() {
		    selected.push($(this).attr('name'));
		});

		for(var i=0; i<selected.length;i++){
			$("#"+selected[i]).removeAttr('checked');
		}

		var $clone = $block.clone();
		$clone.appendTo("#addGroups");
		totalGroups++;
		groupID = "group-" + String(totalGroups);

		var newGroup = $("#addGroups :last-child");
		newGroup.attr("id", groupID);
		$("#addGroups :last-child :nth-child(2)").contents().first().replaceWith("Group "+String(totalGroups));

		console.log($(".groupLabels").css("position"));
	});

	$("#deleteOneGroup").click(function() {
		if (totalGroups > 2) {

			var newLastGroup = document.getElementById("group-" + String(totalGroups-1));
			newLastGroup.nextElementSibling.remove();

			totalGroups--;
		}
	});

	document.getElementById("gettopword").disabled = true;
});
