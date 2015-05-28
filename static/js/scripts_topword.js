$(function() {

	var totalGroups = 2, groupID;

	$("#addOneGroup").click(function() {
		$("#group-2").clone().appendTo("#addGroups");
		totalGroups++;
		groupID = "group-" + String(totalGroups);

		var newGroup = $("#addGroups :last-child");
		newGroup.attr("id", groupID);

		$("#addGroups :last-child :nth-child(2)").contents().first().replaceWith("Group "+String(totalGroups));
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
